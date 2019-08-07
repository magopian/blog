Title: Making a pong game in elm (3)
Date: 2019-08-06 14:03
Category: elm
Tags: gamedev


Following the [two]({filename}/making-a-pong-game-in-elm.md)
[previous]({filename}/making-a-pong-game-in-elm-2.md) blog posts, let's
continue taking tiny steps in our endeavour to create a pong game in elm.

We left off with a ball bouncing off two paddles, and two players able to move
their paddles. And the realization that we were a long way off to have a game
that is at least mildly enjoyable.

## Moving paddles at the same time

For starters, only one player at a time could move their paddle. And this is
because we only moved the paddle when we would detect a `onKeyDown`. Which
meant that we depended on a continuous stream of those events to continuously
move the paddle when a player would keep pressing the key.

But we saw in the previous post that when a player would press a key and hold
it, the events for this key would stop as soon as another key is pressed (eg if
the second player wanted to move their paddle).

After some [digging around on the internet](https://stackoverflow.com/questions/5203407/how-to-detect-if-multiple-keys-are-pressed-at-once-using-javascript)
it seems that the proper way to deal with that issue is to keep track of which
key has been pressed (by tracking the `onKeyDown` events), and then update the
state of this key when an `onKeyUp` is received.

One way to do that would be to store the pressed keys in a list, and then
remove a key from the list once we detect that it's released.
Another way would be track the key states in a dictionnary:

```elm
type KeyState
    = Pressed
    | NotPressed

type alias keyStates =
    { arrowUp : KeyState
    , arrowDown : KeyState
    , charE : KeyState
    , charD : KeyState
    }
```

Thinking about that a bit more: what if we have the following `keyState`:

```elm
    { arrowUp = Pressed
    , arrowDown = Pressed
    ...
    }
```

This would mean that we have two keys pressed for the same paddle, how would we
decide what to do with that? Maybe we could have some kind of clever algorithm
that would update that dictionnary...

If you're like me, you try to stay away from any clever code. As stated by
[Brian Kernighan](http://en.wikipedia.org/wiki/Brian_Kernighan)

> Everyone knows that debugging is twice as hard as writing a program in the
> first place. So if you're as clever as you can be when you write it, how will
> you ever debug it?

— The Elements of Programming Style, 2nd edition, chapter 2

Maybe we could come up with some other representation of the state. How about
storing the state of the paddles movement?

```elm
type PaddleMovement
    = MovingUp
    | MovingDown
    | NotMoving
```

This way, whenever we get an `onKeyDown` for a key, we would update the paddle
movement: pressing down would result in `MovingDown`, and then pressing up
(even if we're still pressing down) would update the movement to `MovingUp`,
and any `onKeyUp` would reset the state to `NotMoving`.

```diff
     { ball : Ball
     , rightPaddle : Paddle
     , leftPaddle : Paddle
+    , rightPaddleMovement : PaddleMovement
+    , leftPaddleMovement : PaddleMovement
     }
 
 
@@ -35,6 +37,12 @@ type alias PaddleInfo =
     }
 
 
+type PaddleMovement
+    = MovingUp
+    | MovingDown
+    | NotMoving
+
+
 type Msg
     = OnAnimationFrame Float
     | KeyDown PlayerAction
@@ -56,6 +64,8 @@ init _ =
     ( { ball = initBall
       , rightPaddle = RightPaddle <| initPaddle 480
       , leftPaddle = LeftPaddle <| initPaddle 10
+      , rightPaddleMovement = NotMoving
+      , leftPaddleMovement = NotMoving
       }
     , Cmd.none
     )
```

[commit](https://github.com/magopian/elm-pong/commit/f46483f7711aef199228090ecc9b26afe2db2c14)

Now we need to update the state in the `update` function, in the `KeyDown
playerAction` case:


```diff
         KeyDown playerAction ->
             case playerAction of
                 RightPaddleUp ->
-                    ( { model | rightPaddle = model.rightPaddle |> updatePaddle -10 }
+                    ( { model | rightPaddleMovement = MovingUp }
                     , Cmd.none
                     )
 
                 RightPaddleDown ->
-                    ( { model | rightPaddle = model.rightPaddle |> updatePaddle 10 }
+                    ( { model | rightPaddleMovement = MovingDown }
                     , Cmd.none
                     )
 
                 LeftPaddleUp ->
-                    ( { model | leftPaddle = model.leftPaddle |> updatePaddle -10 }
+                    ( { model | leftPaddleMovement = MovingUp }
                     , Cmd.none
                     )
 
                 LeftPaddleDown ->
-                    ( { model | leftPaddle = model.leftPaddle |> updatePaddle 10 }
+                    ( { model | leftPaddleMovement = MovingDown }
                     , Cmd.none
                     )
```

[commit](https://github.com/magopian/elm-pong/commit/eee13b34387f11dcea7d8bf3b4aeb51f4662335f)

We're updating the paddle movements, or directions... but we aren't actually
moving them. We used to add or substract a number of pixels from their `y`
coordinates directly on the `KeyDown playerAction` message, but it's not the
case anymore.

Updating the movements, reacting to player inputs, updating the world and all
that is usually done in a "game loop". The closer we have to a game loop in our
program is the `onAnimationFrameDelta` message. So we'll first update our
helper function `updatePaddle` to take a `PaddleMovement` instead of an amount:

```diff
-updatePaddle : Int -> Paddle -> Paddle
-updatePaddle amount paddle =
+updatePaddle : PaddleMovement -> Paddle -> Paddle
+updatePaddle movement paddle =
+    let
+        amount =
+            case movement of
+                MovingUp ->
+                    -10
+
+                MovingDown ->
+                    10
+
+                NotMoving ->
+                    0
+    in
     case paddle of
         RightPaddle paddleInfo ->
             { paddleInfo | y = paddleInfo.y + amount }
```

And we can now use that in the `update` function:

```diff
                         | x = ball.x + horizSpeed
                         , horizSpeed = horizSpeed
                     }
+
+                updatedRightPaddle =
+                    updatePaddle model.rightPaddleMovement model.rightPaddle
+
+                updatedLeftPaddle =
+                    updatePaddle model.leftPaddleMovement model.leftPaddle
             in
-            ( { model | ball = updatedBall }, Cmd.none )
+            ( { model
+                | ball = updatedBall
+                , rightPaddle = updatedRightPaddle
+                , leftPaddle = updatedLeftPaddle
+              }
+            , Cmd.none
+            )
 
         KeyDown playerAction ->
             case playerAction of
```

[commit](https://github.com/magopian/elm-pong/commit/522243fb0aca0faec6b8af6889562c59597d0c0e)

And we're now done, both paddles can move at the same time!

![Both paddles moving at the same time]({static}/images/elm-pong_both_paddles_same_time.gif)

What is it that you're saying? That I forgot to manage the case when there's no
player action anymore? Of course I didn't, I just wanted to make sure you were
still following along. And you were, well done. I never doubted you.

We now need to also subscribe to the `onKeyUp` events for the keys we're using
for the player actions, which means adding

- a `KeyUp PlayerAction` variant to the `Msg` type
- a `case` to the `update` function to deal with this new message
- a new subscription to the `Browser.Events.onKeyUp` events

```diff
 type Msg
     = OnAnimationFrame Float
     | KeyDown PlayerAction
+    | KeyUp PlayerAction
 
 
 type PlayerAction
@@ -160,6 +161,28 @@ update msg model =
                     , Cmd.none
                     )
 
+        KeyUp playerAction ->
+            case playerAction of
+                RightPaddleUp ->
+                    ( { model | rightPaddleMovement = NotMoving }
+                    , Cmd.none
+                    )
+
+                RightPaddleDown ->
+                    ( { model | rightPaddleMovement = NotMoving }
+                    , Cmd.none
+                    )
+
+                LeftPaddleUp ->
+                    ( { model | leftPaddleMovement = NotMoving }
+                    , Cmd.none
+                    )
+
+                LeftPaddleDown ->
+                    ( { model | leftPaddleMovement = NotMoving }
+                    , Cmd.none
+                    )
+
 
 updatePaddle : PaddleMovement -> Paddle -> Paddle
 updatePaddle movement paddle =
@@ -248,6 +271,7 @@ subscriptions _ =
     Sub.batch
         [ Browser.Events.onAnimationFrameDelta OnAnimationFrame
         , Browser.Events.onKeyDown (Decode.map KeyDown keyDecoder)
+        , Browser.Events.onKeyUp (Decode.map KeyUp keyDecoder)
         ]
```

[commit](https://github.com/magopian/elm-pong/commit/b894e75dffa09215f822fb24d5dc63c2cfd2885d)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/8-move-paddles-same-time).


## Clamping the paddles

While it may be fun at first to be able to move your paddle off the screen, and
while it may be seen as an extra challenge, let's stick to the original
concept, and prevent the paddles from disappearing.

We can do that by making sure we don't update the paddle's `y` position with a
value that's "out of bounds":

```diff
     in
     case paddle of
         RightPaddle paddleInfo ->
-            { paddleInfo | y = paddleInfo.y + amount }
+            { paddleInfo
+                | y =
+                    paddleInfo.y
+                        + amount
+                        |> clamp 0 (500 - paddleInfo.height)
+            }
                 |> RightPaddle
 
         LeftPaddle paddleInfo ->
-            { paddleInfo | y = paddleInfo.y + amount }
+            { paddleInfo
+                | y =
+                    paddleInfo.y
+                        + amount
+                        |> clamp 0 (500 - paddleInfo.height)
+            }
                 |> LeftPaddle
```

[commit](https://github.com/magopian/elm-pong/commit/ee829a9d773d6f7f6dd0c6dafafb74489e890af4)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/9-clamp-paddles).

Here we're using the very convenient
[clamp](https://package.elm-lang.org/packages/elm/core/latest/Basics#clamp)
helper to make sure the `y` coordinates of the paddles can't go above `500 -
paddle.height` (which means the full paddle is always displayed), nor below 0.


## Adding some verticalization

Up till now the ball would always move horizontally. Never up or down. And as
such, the game... well, let's say that it wasn't very challenging. But that
changes now!

Let's add a `vertSpeed` to the `ball`, and set it to a fixed value for now:

```diff
@@ -21,6 +21,7 @@ type alias Ball =
     , y : Int
     , radius : Int
     , horizSpeed : Int
+    , vertSpeed : Int
     }
 
 
@@ -78,6 +79,7 @@ initBall =
     , y = 250
     , radius = 10
     , horizSpeed = 4
+    , vertSpeed = 2
     }
 
 
@@ -122,6 +124,7 @@ update msg model =
                 updatedBall =
                     { ball
                         | x = ball.x + horizSpeed
+                        , y = ball.y + ball.vertSpeed
                         , horizSpeed = horizSpeed
                     }
```

[commit](https://github.com/magopian/elm-pong/commit/1098a7ddfc8f815b486bb1f4bf6bd0ae3c8bfd94)

We're not doing anything fancy here: adding a new field to the `Ball` record,
initializing it to `2`, and adding it to the `y` coordinates of the ball on
each frame.

And behold the result!

![Ball moving with a vertical speed]({static}/images/elm-pong_vertical_ball.gif)

And now we know what we need to do next:

## Bouncing the ball off the walls

What good is a ball that we can't see anymore? Let's fix that by mimicking what
we did for the bouncing off the paddles:

```diff
                     else
                         ball.horizSpeed
 
+                shouldBounceVertically =
+                    shouldBallBounceVertically model.ball
+
+                vertSpeed =
+                    if shouldBounceVertically then
+                        ball.vertSpeed * -1
+
+                    else
+                        ball.vertSpeed
+
                 updatedBall =
                     { ball
                         | x = ball.x + horizSpeed
-                        , y = ball.y + ball.vertSpeed
+                        , y = ball.y + vertSpeed
                         , horizSpeed = horizSpeed
+                        , vertSpeed = vertSpeed
                     }
 
                 updatedRightPaddle =
@@ -233,6 +244,15 @@ shouldBallBounce paddle ball =
                 && (ball.y <= y + height)
 
 
+shouldBallBounceVertically : Ball -> Bool
+shouldBallBounceVertically ball =
+    let
+        radius =
+            ball.radius
+    in
+    ball.y <= radius || ball.y >= (500 - radius)
+
+
 view : Model -> Svg.Svg Msg
 view { ball, rightPaddle, leftPaddle } =
     svg
```

[commit](https://github.com/magopian/elm-pong/commit/09af771d95ca043f6ba24cc60d36e93d0febf046)


## Losing and winning

Whenever the ball reaches the left or right side of the screen, the game should
reset, and the opposite player should win a point.

So let's detect the win/lose condition:

```diff
@@ -44,6 +44,11 @@ type PaddleMovement
     | NotMoving
 
 
+type Player
+    = LeftPlayer
+    | RightPlayer
+
+
 type Msg
     = OnAnimationFrame Float
     | KeyDown PlayerAction
@@ -144,6 +149,10 @@ update msg model =
 
                 updatedLeftPaddle =
                     updatePaddle model.leftPaddleMovement model.leftPaddle
+
+                winner =
+                    maybeWinner updatedBall
+                        |> Debug.log "Winner"
             in
             ( { model
                 | ball = updatedBall
@@ -253,6 +262,18 @@ shouldBallBounceVertically ball =
     ball.y <= radius || ball.y >= (500 - radius)
 
 
+maybeWinner : Ball -> Maybe Player
+maybeWinner ball =
+    if ball.x <= ball.radius then
+        Just RightPlayer
+
+    else if ball.x >= (500 - ball.radius) then
+        Just LeftPlayer
+
+    else
+        Nothing
+
+
 view : Model -> Svg.Svg Msg
 view { ball, rightPaddle, leftPaddle } =
     svg
```

[commit](https://github.com/magopian/elm-pong/commit/70edf149c9bb77cc59de4126c4e2c7febd8844e3)

This displays `Winner: Nothing` in the console on each frame, until there's a
`Winner: Just RightPlayer` as soon as the ball hits the right border... and
then on each following frame, as the game doesn't reset. Yet.

"But Mathieu, what is this `Maybe` thing, and all that `Just` and `Nothing`
nonsense?".
Hoy! Behave, that's no nonsense, that's proper engineering! It's called the
[Maybe type](https://package.elm-lang.org/packages/elm/core/latest/Maybe) and
it represents "values that may or may not exist", which is exactly what we need
here: there may be a winner, or maybe not. The result is either "just a player"
or "nothing" (no winner). And we can now use this `Maybe Player` to update a
new custom type that we'll call `GameStatus`:

```diff
@@ -13,6 +13,7 @@ type alias Model =
     , leftPaddle : Paddle
     , rightPaddleMovement : PaddleMovement
     , leftPaddleMovement : PaddleMovement
+    , gameStatus : GameStatus
     }
 
 
@@ -49,6 +50,11 @@ type Player
     | RightPlayer
 
 
+type GameStatus
+    = NoWinner
+    | Winner Player
+
+
 type Msg
     = OnAnimationFrame Float
     | KeyDown PlayerAction
@@ -73,6 +79,7 @@ init _ =
       , leftPaddle = LeftPaddle <| initPaddle 10
       , rightPaddleMovement = NotMoving
       , leftPaddleMovement = NotMoving
+      , gameStatus = NoWinner
       }
     , Cmd.none
     )
@@ -150,14 +157,19 @@ update msg model =
                 updatedLeftPaddle =
                     updatePaddle model.leftPaddleMovement model.leftPaddle
 
-                winner =
-                    maybeWinner updatedBall
-                        |> Debug.log "Winner"
+                gameStatus =
+                    case maybeWinner updatedBall of
+                        Nothing ->
+                            NoWinner
+
+                        Just player ->
+                            Winner player
             in
             ( { model
                 | ball = updatedBall
                 , rightPaddle = updatedRightPaddle
                 , leftPaddle = updatedLeftPaddle
+                , gameStatus = gameStatus
               }
             , Cmd.none
             )
```

[commit](https://github.com/magopian/elm-pong/commit/583616d83b7371cce1fe2e79647b96ea57eea9a1)

We now have a proper `GameState` that gets updated whenever the ball reaches
the left or right, but we aren't doing anything with it yet. What should we do
with it?

Well... if we're in the `NoWinner` state, it means we should be playing, and as
such listening to user input and animation frames. If we're in the `Winner ...`
state, we shouldn't.

```diff
 subscriptions : Model -> Sub Msg
-subscriptions _ =
-    Sub.batch
-        [ Browser.Events.onAnimationFrameDelta OnAnimationFrame
-        , Browser.Events.onKeyDown (Decode.map KeyDown keyDecoder)
-        , Browser.Events.onKeyUp (Decode.map KeyUp keyDecoder)
-        ]
+subscriptions model =
+    case model.gameStatus of
+        NoWinner ->
+            Sub.batch
+                [ Browser.Events.onAnimationFrameDelta OnAnimationFrame
+                , Browser.Events.onKeyDown (Decode.map KeyDown keyDecoder)
+                , Browser.Events.onKeyUp (Decode.map KeyUp keyDecoder)
+                ]
+
+        Winner _ ->
+            Sub.none
```

[commit](https://github.com/magopian/elm-pong/commit/3f529a05544633f974eb0ab55b3a9978b05d4d8b)

As easy as this! Now the game stops as soon as a player wins.

Now let's restart the game after a 500 milliseconds delay. For that, we'll
introduce a new concept: the
[Task](https://package.elm-lang.org/packages/elm/core/latest/Task) which
makes "it easy to describe asynchronous operations": in our case, the `Task`
will be a
[Process.sleep](https://package.elm-lang.org/packages/elm/core/latest/Process#sleep).

Once we have the `Task`, we can ask the elm runtime to execute it for us using
[Task.perform](https://package.elm-lang.org/packages/elm/core/latest/Task#perform)
which will return a [Cmd
Msg](https://package.elm-lang.org/packages/elm/core/latest/Platform-Cmd#Cmd).
We'll attach a new `Msg` variant that we'll call `SleepDone` to that `Cmd`:

```diff
 import Browser
 import Browser.Events
 import Json.Decode as Decode
+import Process
 import Svg exposing (..)
 import Svg.Attributes exposing (..)
+import Task
 
 
 type alias Model =
@@ -59,6 +61,7 @@ type Msg
     = OnAnimationFrame Float
     | KeyDown PlayerAction
     | KeyUp PlayerAction
+    | SleepDone ()
 
 
 type PlayerAction
@@ -157,13 +160,18 @@ update msg model =
                 updatedLeftPaddle =
                     updatePaddle model.leftPaddleMovement model.leftPaddle
 
-                gameStatus =
+                ( gameStatus, cmd ) =
                     case maybeWinner updatedBall of
                         Nothing ->
-                            NoWinner
+                            ( NoWinner, Cmd.none )
 
                         Just player ->
-                            Winner player
+                            let
+                                delayCmd =
+                                    Process.sleep 500
+                                        |> Task.perform SleepDone
+                            in
+                            ( Winner player, delayCmd )
             in
             ( { model
                 | ball = updatedBall
@@ -171,7 +179,7 @@ update msg model =
                 , leftPaddle = updatedLeftPaddle
                 , gameStatus = gameStatus
               }
-            , Cmd.none
+            , cmd
             )
 
         KeyDown playerAction ->
@@ -218,6 +226,13 @@ update msg model =
                     , Cmd.none
                     )
 
+        SleepDone _ ->
+            let
+                _ =
+                    Debug.log "restart" "game"
+            in
+            ( model, Cmd.none )
+
 
 updatePaddle : PaddleMovement -> Paddle -> Paddle
 updatePaddle movement paddle =
```

[commit](https://github.com/magopian/elm-pong/commit/fdcaa7f9437ff5236ea22b108b88898f20f6a995)

This one involves quite a lot, so let's decompose it piece by piece:

On each frame, we now not only change the game status if needed, we also send a
`Cmd` to the elm runtime if there was a win.
This command is:

```elm
Process.sleep 500
    |> Task.perform SleepDone
```

As a reminder, that's the same as writing

```elm
Task.perform SleepDone (Process.sleep 500)
```

The `Task.perform` translates a `Task` into a `Cmd`, which can then be sent to
the elm runtime, by returning it from the `update` function. Which brings us to
the `( Model, Cmd Msg )` in the type signature of the `update` function, which
is a
[tuple type](https://package.elm-lang.org/packages/elm/core/latest/Tuple). A
`tuple` is a fixed size list of things with types which may differ. This is
very different from the
[List type](https://package.elm-lang.org/packages/elm/core/latest/List)
which is a variable size list of things of the same type.

Back to the code:

```elm
( gameStatus, cmd ) =
    case maybeWinner updatedBall of
        Nothing ->
            ( NoWinner, Cmd.none )

        Just player ->
            let
                delayCmd =
                    Process.sleep 500
                        |> Task.perform SleepDone
            in
            ( Winner player, delayCmd )
```

The first part before the `=` sign is destructuring a 2-tuple into two
variables names `gameStatus` and `cmd`. The `cmd` is the command that will be
returned by the `update` function if we're processing an
`onAnimationFrameDelta` message.

And this command is either `Cmd.none` (no command) if there's `NoWinner`, or
the `delayCmd` if there's a winner.

The end of the previous diff is simply processing the `SleepDone` message. At
the moment the only thing it's doing is printing a debug message in the
console. As we've seen previously, using the `_` means we don't care about the
variable (so we don't care about the `"game"` string that we passed to the
`Debug.log` function, and we don't care either about the data attached to the
`SleepDone` message).

"But wait Mathieu, if we don't care about the data attached to the `SleepDone`
variant, why does it even have it in the first place?". Very good question.
Brace yourselves for the answer:

A task always returns something. Sometimes, this "thing" is uninteresting, in
which case we use the `unit`, which is represented by `()` and has only one
value: `()`. And if we go back to the `Process.sleep` signature, it says
it returns a `Task x ()` (so a `Task` that returns a unit).

And this thing that the `Task` returns is the same thing that is attached to the
message that the `Task.perform` takes as its first argument. Hence the
`SleepDone ()`.

Let me show you a little nugget of cleverness (but please remember, being
clever is usually a bad idea, so use this sparingly):
[the `always` helper](https://package.elm-lang.org/packages/elm/core/latest/Basics#always)
is a function that always returns the same thing, whatever the argument you
give it. This seems pretty useless, but we could use it to our advantage in our
case:

```diff
@@ -61,7 +61,7 @@ type Msg
     = OnAnimationFrame Float
     | KeyDown PlayerAction
     | KeyUp PlayerAction
-    | SleepDone ()
+    | SleepDone
 
 
 type PlayerAction
@@ -169,7 +169,7 @@ update msg model =
                             let
                                 delayCmd =
                                     Process.sleep 500
-                                        |> Task.perform SleepDone
+                                        |> Task.perform (always SleepDone)
                             in
                             ( Winner player, delayCmd )
             in
@@ -226,7 +226,7 @@ update msg model =
                     , Cmd.none
                     )
 
-        SleepDone _ ->
+        SleepDone ->
             let
                 _ =
                     Debug.log "restart" "game"
```

We don't care about the data attached to the message by `Task.perform`, so we
just discard it by using the `always` helper. This might seem confusing, but
keep in mind that a custom type variant is also a constructor. So when we
wanted to create a new right paddle, we would do `RightPaddle paddleInfo`.
You can see `RightPaddle` as a function with the following type signature:

`RightPaddle : PaddleInfo -> Paddle`

So you can also see `(always SleepDone)` as a function that takes a parameter
and returns `SleepDone`, and we could call it `alwaysSleepDone`:

`alwaysSleepDone : a -> Msg`

Using a type starting with a lowercase (the `a` in the type signature just
above) means that it could be any type, including an `unit`. In any case, we
don't care about the type that's being passed to the helper, so no need to be
specific here.

So the final diff would be:

```diff
@@ -61,7 +61,7 @@ type Msg
     = OnAnimationFrame Float
     | KeyDown PlayerAction
     | KeyUp PlayerAction
-    | SleepDone ()
+    | SleepDone
 
 
 type PlayerAction
@@ -167,9 +167,13 @@ update msg model =
 
                         Just player ->
                             let
+                                alwaysSleepDone : a -> Msg
+                                alwaysSleepDone =
+                                    always SleepDone
+
                                 delayCmd =
                                     Process.sleep 500
-                                        |> Task.perform SleepDone
+                                        |> Task.perform alwaysSleepDone
                             in
                             ( Winner player, delayCmd )
             in
@@ -226,7 +230,7 @@ update msg model =
                     , Cmd.none
                     )
 
-        SleepDone _ ->
+        SleepDone ->
             let
                 _ =
                     Debug.log "restart" "game"
```

[commit](https://github.com/magopian/elm-pong/commit/1ab844992f82f875f31fca402070ee626b11d106)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/10-win-lose).

This didn't give us much in terms of readability, or at least it's debatable. I
know I'd rather have obvious types and slightly more complex code, but I guess
that's a matter of taste.


## Restarting the game

So what should happen once the delay has elapsed, and the game should
"restart"? Well the ball should be reset to its initial position and speed, and
the game status should be `NoWinner` again:

```diff
         SleepDone ->
-            let
-                _ =
-                    Debug.log "restart" "game"
-            in
-            ( model, Cmd.none )
+            ( { model
+                | ball = initBall
+                , gameStatus = NoWinner
+              }
+            , Cmd.none
+            )
```

[commit](https://github.com/magopian/elm-pong/commit/49ca518a40f427c0b6f7fd24c2493522e568fe8f)

Once the ball touches one of the "goals", the whole game stops for half a
second, and then the ball position is reset.


## Keeping track of the score

Let's add a `score` record with the `rightPlayerScore` and `leftPlayerScore`
fields to the model, and update them whenever there's a win:

```diff
@@ -16,6 +16,7 @@ type alias Model =
     , rightPaddleMovement : PaddleMovement
     , leftPaddleMovement : PaddleMovement
     , gameStatus : GameStatus
+    , score : Score
     }
 
 
@@ -71,6 +72,12 @@ type PlayerAction
     | LeftPaddleDown
 
 
+type alias Score =
+    { rightPlayerScore : Int
+    , leftPlayerScore : Int
+    }
+
+
 type alias Flags =
     ()
 
@@ -83,6 +90,10 @@ init _ =
       , rightPaddleMovement = NotMoving
       , leftPaddleMovement = NotMoving
       , gameStatus = NoWinner
+      , score =
+            { rightPlayerScore = 0
+            , leftPlayerScore = 0
+            }
       }
     , Cmd.none
     )
@@ -160,10 +171,10 @@ update msg model =
                 updatedLeftPaddle =
                     updatePaddle model.leftPaddleMovement model.leftPaddle
 
-                ( gameStatus, cmd ) =
+                ( gameStatus, score, cmd ) =
                     case maybeWinner updatedBall of
                         Nothing ->
-                            ( NoWinner, Cmd.none )
+                            ( NoWinner, model.score, Cmd.none )
 
                         Just player ->
                             let
@@ -174,14 +185,19 @@ update msg model =
                                 delayCmd =
                                     Process.sleep 500
                                         |> Task.perform alwaysSleepDone
+
+                                updatedScore =
+                                    updateScores model.score player
+                                        |> Debug.log "score"
                             in
-                            ( Winner player, delayCmd )
+                            ( Winner player, updatedScore, delayCmd )
             in
             ( { model
                 | ball = updatedBall
                 , rightPaddle = updatedRightPaddle
                 , leftPaddle = updatedLeftPaddle
                 , gameStatus = gameStatus
+                , score = score
               }
             , cmd
             )
@@ -306,6 +322,16 @@ maybeWinner ball =
         Nothing
 
 
+updateScores : Score -> Player -> Score
+updateScores score winner =
+    case winner of
+        RightPlayer ->
+            { score | rightPlayerScore = score.rightPlayerScore + 1 }
+
+        LeftPlayer ->
+            { score | leftPlayerScore = score.leftPlayerScore + 1 }
+
+
 view : Model -> Svg.Svg Msg
 view { ball, rightPaddle, leftPaddle } =
     svg
```

[commit](https://github.com/magopian/elm-pong/commit/84d0867a619fde6032c5563e28542606ff0ecd4a)

Now that we have the score, we can display it ;)

```diff
@@ -188,7 +188,6 @@ update msg model =
 
                                 updatedScore =
                                     updateScores model.score player
-                                        |> Debug.log "score"
                             in
                             ( Winner player, updatedScore, delayCmd )
             in
@@ -333,7 +332,7 @@ updateScores score winner =
 
 
 view : Model -> Svg.Svg Msg
-view { ball, rightPaddle, leftPaddle } =
+view { ball, rightPaddle, leftPaddle, score } =
     svg
         [ width "500"
         , height "500"
@@ -343,6 +342,7 @@ view { ball, rightPaddle, leftPaddle } =
         [ viewBall ball
         , viewPaddle rightPaddle
         , viewPaddle leftPaddle
+        , viewScore score
         ]
 
 
@@ -376,6 +376,19 @@ viewPaddle paddle =
         []
 
 
+viewScore : Score -> Svg.Svg Msg
+viewScore score =
+    g
+        [ fontSize "100px"
+        , fontFamily "monospace"
+        ]
+        [ text_ [ x "100", y "100", textAnchor "start" ]
+            [ text <| String.fromInt score.leftPlayerScore ]
+        , text_ [ x "400", y "100", textAnchor "end" ]
+            [ text <| String.fromInt score.rightPlayerScore ]
+        ]
+
+
 subscriptions : Model -> Sub Msg
 subscriptions model =
     case model.gameStatus of
```

[commit](https://github.com/magopian/elm-pong/commit/bbb07a70ec9bd4e2b089cfdb4bba16c3df7c117d)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/11-display-score).

Tada!!!

![Displaying the score]({static}/images/elm-pong_score.png)

Maybe it's time to talk briefly about the view. You might have been wondering
how that was working.

In elm we have packages that provide helpers to build the node tree. There's
one for [Html](https://package.elm-lang.org/packages/elm/html/latest/) and one
for [SVG](https://package.elm-lang.org/packages/elm/svg/latest/Svg), and they
both work the same way.
Each node builder has two parameters:

- a list of attributes and event listeners
- a list of child nodes

One notable exception is the `text` helper which just returns plain text.

This is how you would build a paragraph with the `foobar` class:

```elm
Html.p
    [ Html.Attributes.class "foobar" ]
    [ Html.text "Hello world"]
```

So building a node tree (a DOM) is a matter of calling helpers and providing
them their list of attributes and children.

And that's exactly what we did with the `viewScore` function:

- the parent node is an SVG `<g>` container, with a list of attributes
    - first child is an SVG `<text>` node with its list of attributes
        - and its child is just plain text
    - second child is an SVG `<text>` node with its list of attributes
        - and its child is just plain text

The use of an underscore in `text_` is needed to disambiguate between the
`<text>` SVG node and the plain text helper `text`.

We now have a fully playable game! It might not be pretty, or fun, but it has
all the minimal requirements, congratulations!

Next time, we might have a look at how to add a few bells and whistles just for
the sake of introducing a few more elm concepts ;)

----

There's now a [follow up]({filename}/making-a-pong-game-in-elm-4.md).
