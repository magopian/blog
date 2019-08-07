Title: Making a pong game in elm (4)
Date: 2019-08-07 14:03
Category: elm
Tags: gamedev


Following the [three]({filename}/making-a-pong-game-in-elm.md)
[previous]({filename}/making-a-pong-game-in-elm-2.md)
[blog]({filename}/making-a-pong-game-in-elm-3.md) posts, let's continue taking
tiny steps in our endeavour to create a pong game in elm.


## External contribution from [Rémy](https://github.com/Natim)

Rémy is an former colleague from
[Mozilla](https://github.com/magopian/elm-pong/pulls) and is a wonderful, very
joyful and productive friend. When he saw this series of blog posts, he
contributed a few [issues](https://github.com/magopian/elm-pong/issues) and
[pull requests](https://github.com/magopian/elm-pong/pulls) to the project,
thanks!

The [first PR](https://github.com/magopian/elm-pong/pull/1/files) is to fix a
corner case where the ball would be "trapped" by the paddle: if the paddle
catches the ball before it touches the side, the ball bounces back and forth on
each frame. To fix that, the trick is to also check the direction the ball is
going, and only bounce if it's going towards the side the paddle is on:

```diff
             (ball.x - ball.radius <= x + width)
                 && (ball.y >= y)
                 && (ball.y <= y + height)
+                && (ball.horizSpeed < 0)
 
         RightPaddle { x, y, height } ->
             (ball.x + ball.radius >= x)
                 && (ball.y >= y)
                 && (ball.y <= y + height)
+                && (ball.horizSpeed > 0)
```

[commit](https://github.com/magopian/elm-pong/commit/dc535518fa478a7ff403f8e792b336c5bbea0209)

The [second PR](https://github.com/magopian/elm-pong/pull/2/files) is a bit
more involved: it's not related to the game itself, but rather to how people
can interact and contribute to it.

Adding a few helper scripts is convenient to newcomers, and having a `npm run
deploy` helps with automating the upload to the
[github pages](https://magopian.github.io/elm-pong/) where the most up to date
version is playable.

Now for the issues. The
[second one](https://github.com/magopian/elm-pong/issues/4) is an issue I
spotted but didn't get around to fixing yet. Here's how to reproduce it:

- one player presses and keeps pressing a key (eg: the down arrow)
- as the paddle moves down, the game is restarted (because one of the two
  players won)
- while the game is paused (the 500ms delay), the key is released (eg: the down
  arrow is released)
- once the game is restarted, the paddle moves down on its own, even though the
  down arrow is released

The reason is pretty obvious: during the pause we're not subscribed to the
`onKeyUp` events so we don't update the `PaddleMovement`.

There's an easy way to fix that: reset the paddles (position and movement) once
the game restarts:

```diff
         SleepDone ->
             ( { model
                 | ball = initBall
+                , rightPaddle = RightPaddle <| initPaddle 480
+                , leftPaddle = LeftPaddle <| initPaddle 10
+                , rightPaddleMovement = NotMoving
+                , leftPaddleMovement = NotMoving
                 , gameStatus = NoWinner
               }
             , Cmd.none
```

[commit](https://github.com/magopian/elm-pong/commit/661a31e4bf082cae5c74aa1840541933c5e4a22a)

Another way would have been to keep being subscribed to the key events even
during the pause, but that wouldn't have been sufficient: during the pause we
don't subscribe to the animation frame events anymore, and as such our "game
loop" is on pause, and we don't update anything anymore.

So instead of changing the subscription, we'd have to do a `case` on the
`GameStatus` when updating the ball, and only update it while there's no
winner:

```diff
                         ball.vertSpeed
 
                 updatedBall =
-                    { ball
-                        | x = ball.x + horizSpeed
-                        , y = ball.y + vertSpeed
-                        , horizSpeed = horizSpeed
-                        , vertSpeed = vertSpeed
-                    }
+                    case model.gameStatus of
+                        Winner _ ->
+                            ball
+
+                        NoWinner ->
+                            { ball
+                                | x = ball.x + horizSpeed
+                                , y = ball.y + vertSpeed
+                                , horizSpeed = horizSpeed
+                                , vertSpeed = vertSpeed
+                            }
 
                 updatedRightPaddle =
                     updatePaddle model.rightPaddleMovement model.rightPaddle
@@ -248,10 +253,6 @@ update msg model =
         SleepDone ->
             ( { model
                 | ball = initBall
-                , rightPaddle = RightPaddle <| initPaddle 480
-                , leftPaddle = LeftPaddle <| initPaddle 10
-                , rightPaddleMovement = NotMoving
-                , leftPaddleMovement = NotMoving
                 , gameStatus = NoWinner
               }
             , Cmd.none
@@ -397,16 +398,11 @@ viewScore score =
 
 subscriptions : Model -> Sub Msg
 subscriptions model =
-    case model.gameStatus of
-        NoWinner ->
-            Sub.batch
-                [ Browser.Events.onAnimationFrameDelta OnAnimationFrame
-                , Browser.Events.onKeyDown (Decode.map KeyDown keyDecoder)
-                , Browser.Events.onKeyUp (Decode.map KeyUp keyDecoder)
-                ]
-
-        Winner _ ->
-            Sub.none
+    Sub.batch
+        [ Browser.Events.onAnimationFrameDelta OnAnimationFrame
+        , Browser.Events.onKeyDown (Decode.map KeyDown keyDecoder)
+        , Browser.Events.onKeyUp (Decode.map KeyUp keyDecoder)
+        ]
```

[commit](https://github.com/magopian/elm-pong/commit/661a31e4bf082cae5c74aa1840541933c5e4a22a)

So we revert our change in the `SleepDone` message (when we restart the game),
and we always subscribe to all the events (animation frame and keys). And
finally we only update the ball when it's not on pause after a win.

However we now have a very weird behaviour:

![Weird behavior on reset]({static}/images/elm-pong_weird_reset.gif)

Well... the game loop runs every animation frame (so roughly 60 times per
second). And on each frame, even when the game is "paused" (actually, just the
ball is paused now) we check if there's a win, and we increase the score, and
start a 500ms delay...

So let's modify the current `case maybeWinner updatedBall` to be:

```diff
                     updatePaddle model.leftPaddleMovement model.leftPaddle
 
                 ( gameStatus, score, cmd ) =
-                    case maybeWinner updatedBall of
-                        Nothing ->
-                            ( NoWinner, model.score, Cmd.none )
-
-                        Just player ->
+                    case ( maybeWinner updatedBall, model.gameStatus ) of
+                        ( Just player, NoWinner ) ->
                             let
                                 alwaysSleepDone : a -> Msg
                                 alwaysSleepDone =
@@ -195,6 +192,9 @@ update msg model =
                                     updateScores model.score player
                             in
                             ( Winner player, updatedScore, delayCmd )
+
+                        _ ->
+                            ( model.gameStatus, model.score, Cmd.none )
             in
             ( { model
                 | ball = updatedBall
```

[commit](https://github.com/magopian/elm-pong/commit/c9cc341ce66ff28c0922a9a2c04ad70569fa939b)

Here the case is on a 2-tuple, and the only special case that interests us is
when we have no winner in the `GameStatus` yet, but we just detected there's a
win. In this case, and only in this case do we increase the score and start a
500ms sleep.
In all the other cases (destructured as `_ ->` here) we just return the
unmodified game status, score, and no commands.

That's now working perfectly. However the code is starting to get really
unreadable in this game loop... Let's see if we can rewrite and refactor it to
make it clearer:

```diff
     case msg of
         OnAnimationFrame timeDelta ->
             let
-                ball =
-                    model.ball
-
-                shouldBounce =
-                    shouldBallBounce model.rightPaddle model.ball
-                        || shouldBallBounce model.leftPaddle model.ball
-
-                horizSpeed =
-                    if shouldBounce then
-                        ball.horizSpeed * -1
-
-                    else
-                        ball.horizSpeed
-
-                shouldBounceVertically =
-                    shouldBallBounceVertically model.ball
-
-                vertSpeed =
-                    if shouldBounceVertically then
-                        ball.vertSpeed * -1
-
-                    else
-                        ball.vertSpeed
-
                 updatedBall =
-                    case model.gameStatus of
-                        Winner _ ->
-                            ball
-
-                        NoWinner ->
-                            { ball
-                                | x = ball.x + horizSpeed
-                                , y = ball.y + vertSpeed
-                                , horizSpeed = horizSpeed
-                                , vertSpeed = vertSpeed
-                            }
-
-                updatedRightPaddle =
-                    updatePaddle model.rightPaddleMovement model.rightPaddle
-
-                updatedLeftPaddle =
-                    updatePaddle model.leftPaddleMovement model.leftPaddle
+                    updateBall model
 
                 ( gameStatus, score, cmd ) =
                     case ( maybeWinner updatedBall, model.gameStatus ) of
@@ -198,8 +158,8 @@ update msg model =
             in
             ( { model
                 | ball = updatedBall
-                , rightPaddle = updatedRightPaddle
-                , leftPaddle = updatedLeftPaddle
+                , rightPaddle = updatePaddle model.rightPaddleMovement model.rightPaddle
+                , leftPaddle = updatePaddle model.leftPaddleMovement model.leftPaddle
                 , gameStatus = gameStatus
                 , score = score
               }
@@ -259,6 +219,50 @@ update msg model =
             )
 
 
+updateBall :
+    { a
+        | gameStatus : GameStatus
+        , ball : Ball
+        , rightPaddle : Paddle
+        , leftPaddle : Paddle
+    }
+    -> Ball
+updateBall { gameStatus, ball, rightPaddle, leftPaddle } =
+    let
+        shouldBounce =
+            shouldBallBounce rightPaddle ball
+                || shouldBallBounce leftPaddle ball
+
+        horizSpeed =
+            if shouldBounce then
+                ball.horizSpeed * -1
+
+            else
+                ball.horizSpeed
+
+        shouldBounceVertically =
+            shouldBallBounceVertically ball
+
+        vertSpeed =
+            if shouldBounceVertically then
+                ball.vertSpeed * -1
+
+            else
+                ball.vertSpeed
+    in
+    case gameStatus of
+        Winner _ ->
+            ball
+
+        NoWinner ->
+            { ball
+                | x = ball.x + horizSpeed
+                , y = ball.y + vertSpeed
+                , horizSpeed = horizSpeed
+                , vertSpeed = vertSpeed
+            }
+
+
 updatePaddle : PaddleMovement -> Paddle -> Paddle
 updatePaddle movement paddle =
     let
```

[commit](https://github.com/magopian/elm-pong/commit/34722dbf26165fec2f9760334b34c0ee57e7afd3)

That's a big one! It looks impressive, but most of it is just moving the code
related to updating the ball (checking if it bounces to update its speed and
moving it) to its own `updateBall` helper.

However there's something worth noting here, and it's in the signature of the
`updateBall`:

```elm
updateBall :
    { a
        | gameStatus : GameStatus
        , ball : Ball
        , rightPaddle : Paddle
        , leftPaddle : Paddle
    }
    -> Ball
updateBall { gameStatus, ball, rightPaddle, leftPaddle } =
```

Up til now we've seen how to write a type signature with various types, but
this is the first time we're seeing this `{ a | ...}` notation. This is an
[extensible record](https://elm-lang.org/docs/records#record-types) (more
information in
[this "Advanced Types in Elm - Extensible Records" blog post by Charlie
Koster](https://medium.com/@ckoster22/advanced-types-in-elm-extensible-records-67e9d804030d)
and the
["Scaling elm apps" talk by Richard Feldman](https://www.youtube.com/watch?v=DoA4Txr4GUs)).

To sum it up, it's a way to

- document which fields are of interest to the function
- narrow the arguments to the function: it'll only take, use or return specific fields from the records
- make a function usable on several different types of records, as long as they have the fields defined in the extensible record

In our case we're mostly using this for the first two use cases.

We're now left with this game status and score update. Those two should
obviously happen together, but it feels a bit alien to have them mixed in the
game loop together with the updating of the paddles.

How awesome would it be to have a `NewWinner Player` message? If we had it, we
could update the game status and the score update in this `case` of the
`update` function, and it would make perfect sense!

"But Mathieu, how do we *send* our own messages to the `update function`?
Aren't messages usually coming from subscriptions, or maybe events like
`onClick` on a button and the like?".

Well, yes, usually the messages are "handed to us" by the elm runtime. And we
could tell the runtime to
[send us such a
message](http://faq.elm-community.org/#how-do-i-generate-a-new-message-as-a-command),
but as you can read from this piece, it's not recommended (check
["How to turn a Msg into a Cmd in Elm?" from Wouter In t Velt](https://medium.com/elm-shorts/how-to-turn-a-msg-into-a-cmd-msg-in-elm-5dd095175d84)
for more information on why).

But if we get back to the original question: how do we send our own messages to
the `update` **function**?

Well, the `update` function is just that: a function. And a function can be
called, for example with our own `NewWinner Player` message, and the updated
model we get in the "game loop":

```diff
@@ -63,6 +63,7 @@ type Msg
     | KeyDown PlayerAction
     | KeyUp PlayerAction
     | SleepDone
+    | NewWinner Player
 
 
 type PlayerAction
@@ -136,34 +137,32 @@ update msg model =
                 updatedBall =
                     updateBall model
 
-                ( gameStatus, score, cmd ) =
-                    case ( maybeWinner updatedBall, model.gameStatus ) of
-                        ( Just player, NoWinner ) ->
-                            let
-                                alwaysSleepDone : a -> Msg
-                                alwaysSleepDone =
-                                    always SleepDone
-
-                                delayCmd =
-                                    Process.sleep 500
-                                        |> Task.perform alwaysSleepDone
-
-                                updatedScore =
-                                    updateScores model.score player
-                            in
-                            ( Winner player, updatedScore, delayCmd )
-
-                        _ ->
-                            ( model.gameStatus, model.score, Cmd.none )
+                updatedModel =
+                    { model
+                        | ball = updatedBall
+                        , rightPaddle = updatePaddle model.rightPaddleMovement model.rightPaddle
+                        , leftPaddle = updatePaddle model.leftPaddleMovement model.leftPaddle
+                    }
             in
-            ( { model
-                | ball = updatedBall
-                , rightPaddle = updatePaddle model.rightPaddleMovement model.rightPaddle
-                , leftPaddle = updatePaddle model.leftPaddleMovement model.leftPaddle
-                , gameStatus = gameStatus
-                , score = score
-              }
-            , cmd
+            case ( maybeWinner updatedBall, model.gameStatus ) of
+                ( Just player, NoWinner ) ->
+                    update (NewWinner player) updatedModel
+
+                _ ->
+                    ( updatedModel, Cmd.none )
+
+        NewWinner player ->
+            let
+                alwaysSleepDone : a -> Msg
+                alwaysSleepDone =
+                    always SleepDone
+
+                updatedScore =
+                    updateScores model.score player
+            in
+            ( { model | gameStatus = Winner player, score = updatedScore }
+            , Process.sleep 500
+                |> Task.perform alwaysSleepDone
             )
 
         KeyDown playerAction ->
```

[commit](https://github.com/magopian/elm-pong/commit/abbaf2d90ba81d37158945abf010475e9b301696)

What we did here is:

- in the game loop, update the ball and the paddles
- make an updated model with those updates
- if there's no new winner, return that updated model
- if there's a new winner, return the result of a call to the `update` function
  with our `NewWinner Player` message and the updated model

While we're rewriting and refactoring parts of the `update` function, let's
rename this `SleepDone` message wich isn't very meaningful to `RestartGame`
instead:

```diff
     = OnAnimationFrame Float
     | KeyDown PlayerAction
     | KeyUp PlayerAction
-    | SleepDone
+    | RestartGame
     | NewWinner Player
 
 
@@ -153,16 +153,16 @@ update msg model =
 
         NewWinner player ->
             let
-                alwaysSleepDone : a -> Msg
-                alwaysSleepDone =
-                    always SleepDone
+                alwaysRestartGame : a -> Msg
+                alwaysRestartGame =
+                    always RestartGame
 
                 updatedScore =
                     updateScores model.score player
             in
             ( { model | gameStatus = Winner player, score = updatedScore }
             , Process.sleep 500
-                |> Task.perform alwaysSleepDone
+                |> Task.perform alwaysRestartGame
             )
 
         KeyDown playerAction ->
@@ -209,7 +209,7 @@ update msg model =
                     , Cmd.none
                     )
 
-        SleepDone ->
+        RestartGame ->
             ( { model
                 | ball = initBall
                 , gameStatus = NoWinner
```

[commit](https://github.com/magopian/elm-pong/commit/b88ffa27688628881cc89a96a5034deb7224d6f8)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/12-external-contributions).

We're now in a much better place!


## Non linear paddles

If we look back at the
[original gameplay](https://www.youtube.com/watch?v=it0sf4CMDeM) we see that
the ball doesn't bounce linearily on the paddles. Depending on where it touches
the paddle, the bounce angle varies. This is better explained in
[this tutorial on writing a pong game in unity](https://noobtuts.com/unity/2d-pong-game).

Let's implement that!

When we update the `horizSpeed` when the ball `shouldBounce`, we now also need
to update the `vertSpeed` according to the place where the ball hit the paddle.

The idea is to come up with a "distance" in signed percentage from the center
of the paddle, so we would have -100% for a hit right on the top of the paddle,
and 100% if it's the bottom of the paddle.

Once we have this percentage, we can divide it by 10 to have a vertical speed
between 0 (the ball hits the paddle right in the center) and 10 (the ball hits
the top or the bottom of the paddle).

Here's the modified `updateBall` function:

```diff
 updateBall { gameStatus, ball, rightPaddle, leftPaddle } =
     let
-        shouldBounce =
-            shouldBallBounce rightPaddle ball
-                || shouldBallBounce leftPaddle ball
+        maybeRightDistance =
+            maybeBounceDistanceFromCenter rightPaddle ball
 
-        horizSpeed =
-            if shouldBounce then
-                ball.horizSpeed * -1
+        maybeLeftDistance =
+            maybeBounceDistanceFromCenter leftPaddle ball
+
+        maybeDistance =
+            -- Combine the two maybes and keep the one that isn't Nothing, if any.
+            if maybeRightDistance == Nothing then
+                maybeLeftDistance
 
             else
-                ball.horizSpeed
+                maybeRightDistance
+
+        ( horizSpeed, bouncedVertSpeed ) =
+            case maybeDistance of
+                Nothing ->
+                    -- No bounce
+                    ( ball.horizSpeed, ball.vertSpeed )
+
+                Just distance ->
+                    ( ball.horizSpeed * -1
+                    , distance // 10
+                    )
 
         shouldBounceVertically =
             shouldBallBounceVertically ball
 
         vertSpeed =
             if shouldBounceVertically then
-                ball.vertSpeed * -1
+                bouncedVertSpeed * -1
 
             else
-                ball.vertSpeed
+                bouncedVertSpeed
     in
     case gameStatus of
         Winner _ ->

```

Nothing fancy here, but maybe the `maybeDistance`: we "combine" both `Maybe`s
by keeping the first one that isn't a `Nothing`. This way we simplify the `case
maybeDistance` and we don't have to duplicate the code that updates the
`horizSpeed` and `vertSpeed` if there's a hit on the left or right paddle.

Now for the hairy `maybeBounceDistanceFromCenter`:

```diff
-shouldBallBounce : Paddle -> Ball -> Bool
-shouldBallBounce paddle ball =
+maybeBounceDistanceFromCenter : Paddle -> Ball -> Maybe Int
+maybeBounceDistanceFromCenter paddle ball =
+    -- If the ball bounces, return Just the distance from the paddle center in
+    -- percentage, so -100% if it's the very top of the paddle, 100% if it's
+    -- the very bottom of the paddle.
+    let
+        normalize : Int -> Int -> Int
+        normalize distance height =
+            (distance - (height // 2)) * 100 // (height // 2)
+    in
     case paddle of
         LeftPaddle { x, y, width, height } ->
-            (ball.x - ball.radius <= x + width)
-                && (ball.y >= y)
-                && (ball.y <= y + height)
-                && (ball.horizSpeed < 0)
+            if
+                (ball.x - ball.radius <= x + width)
+                    && (ball.y >= y)
+                    && (ball.y <= y + height)
+                    && (ball.horizSpeed < 0)
+            then
+                Just <| normalize (ball.y - y) height
+
+            else
+                Nothing
 
         RightPaddle { x, y, height } ->
-            (ball.x + ball.radius >= x)
-                && (ball.y >= y)
-                && (ball.y <= y + height)
-                && (ball.horizSpeed > 0)
+            if
+                (ball.x + ball.radius >= x)
+                    && (ball.y >= y)
+                    && (ball.y <= y + height)
+                    && (ball.horizSpeed > 0)
+            then
+                Just <| normalize (ball.y - y) height
+
+            else
+                Nothing
```

[commit](https://github.com/magopian/elm-pong/commit/434ea02cd02e87897656ef448c7814a6f606ffc6)

Phew, that was a tough one, but we did it!


## Cosmetic changes

Well, it seems we're nearly done! By looking at the original pong we can see
there's a couple of obvious differences still: the ball should be square (which
will make [this issue](https://github.com/magopian/elm-pong/issues/3)
disappear), and there's a dotted line in the center of the screen.

```diff
@@ -23,7 +23,7 @@ type alias Model =
 type alias Ball =
     { x : Int
     , y : Int
-    , radius : Int
+    , size : Int
     , horizSpeed : Int
     , vertSpeed : Int
     }
@@ -104,7 +104,7 @@ initBall : Ball
 initBall =
     { x = 250
     , y = 250
-    , radius = 10
+    , size = 10
     , horizSpeed = 4
     , vertSpeed = 2
     }
@@ -321,7 +321,7 @@ maybeBounceDistanceFromCenter paddle ball =
     case paddle of
         LeftPaddle { x, y, width, height } ->
             if
-                (ball.x - ball.radius <= x + width)
+                (ball.x <= x + width)
                     && (ball.y >= y)
                     && (ball.y <= y + height)
                     && (ball.horizSpeed < 0)
@@ -333,7 +333,7 @@ maybeBounceDistanceFromCenter paddle ball =
 
         RightPaddle { x, y, height } ->
             if
-                (ball.x + ball.radius >= x)
+                (ball.x + ball.size >= x)
                     && (ball.y >= y)
                     && (ball.y <= y + height)
                     && (ball.horizSpeed > 0)
@@ -347,18 +347,18 @@ maybeBounceDistanceFromCenter paddle ball =
 shouldBallBounceVertically : Ball -> Bool
 shouldBallBounceVertically ball =
     let
-        radius =
-            ball.radius
+        size =
+            ball.size
     in
-    ball.y <= radius || ball.y >= (500 - radius)
+    ball.y <= size || ball.y >= (500 - size)
 
 
 maybeWinner : Ball -> Maybe Player
 maybeWinner ball =
-    if ball.x <= ball.radius then
+    if ball.x <= ball.size then
         Just RightPlayer
 
-    else if ball.x >= (500 - ball.radius) then
+    else if ball.x >= (500 - ball.size) then
         Just LeftPlayer
 
     else
@@ -391,11 +391,12 @@ view { ball, rightPaddle, leftPaddle, score } =
 
 
 viewBall : Ball -> Svg.Svg Msg
-viewBall { x, y, radius } =
-    circle
-        [ cx <| String.fromInt x
-        , cy <| String.fromInt y
-        , r <| String.fromInt radius
+viewBall ball =
+    rect
+        [ x <| String.fromInt ball.x
+        , y <| String.fromInt ball.y
+        , width <| String.fromInt ball.size
+        , height <| String.fromInt ball.size
         ]
         []
```

[commit](https://github.com/magopian/elm-pong/commit/869c3592958baf5573c86039228b88f932ebce42)

We renamed the `radius` field of the `Ball` record to be `size` instead which
makes more sense for a square ball, and updated the `viewBall` helper to draw a
rect instead of a circle. We also took the opportunity to fix a small bug, did
you spot it?

Yes, we were checking for `ball.x - ball.radius` for the left paddle... which
meant we were bouncing the ball from the left paddle 10 pixels too early.

And for the screen divider:

```diff
@@ -383,13 +383,28 @@ view { ball, rightPaddle, leftPaddle, score } =
         , viewBox "0 0 500 500"
         , Svg.Attributes.style "background: #efefef"
         ]
-        [ viewBall ball
+        [ viewDivider
+        , viewBall ball
         , viewPaddle rightPaddle
         , viewPaddle leftPaddle
         , viewScore score
         ]
 
 
+viewDivider : Svg.Svg Msg
+viewDivider =
+    line
+        [ x1 "249"
+        , y1 "0"
+        , x2 "249"
+        , y2 "500"
+        , stroke "black"
+        , strokeDasharray "4"
+        , strokeWidth "2"
+        ]
+        []
+
+
 viewBall : Ball -> Svg.Svg Msg
 viewBall ball =
     rect
```

[commit](https://github.com/magopian/elm-pong/commit/fde14ae537d26073a051e17a3922329f3b2d5fcc)

And a final touch: let's move the scores closer to their edges:

```diff
@@ -442,9 +442,9 @@ viewScore score =
         [ fontSize "100px"
         , fontFamily "monospace"
         ]
-        [ text_ [ x "100", y "100", textAnchor "start" ]
+        [ text_ [ x "50", y "100", textAnchor "start" ]
             [ text <| String.fromInt score.leftPlayerScore ]
-        , text_ [ x "400", y "100", textAnchor "end" ]
+        , text_ [ x "450", y "100", textAnchor "end" ]
             [ text <| String.fromInt score.rightPlayerScore ]
         ]
```

[commit](https://github.com/magopian/elm-pong/commit/9b904a55cc8257d12a252a8d7e6722ebbc2dfa90)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/13-original-game).

And now we have it:

![Game that now looks like the original pong]({static}/images/elm-pong_original_look.png)
