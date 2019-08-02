Title: Making a pong game in elm (3)
Date: 2019-08-02 11:01
Category: elm
Tags: gamedev


Following the [two]({filename}/making-a-pong-game-in-elm.md)
[previous]({filename}/making-a-pong-game-in-elm-2.md) blog posts, let's
continue taking tiny steps in our endeavour to create a pong game in elm.

We left off with a ball bouncing off two paddles, and two players able to move
their paddle. And the realization that we were a long way off to have a game
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
state of those keys when an `onKeyUp` is received.

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

In games the updating of the movements, reacting to player inputs and all that
is done in a "game loop". The closer we have in our program is the
`onAnimationFrameDelta` message. So we'll first update our helper function
`updatePaddle` to take a `PaddleMovement` instead of an amount:

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


## Adding some randomization

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

## Bouncing the ball of the walls

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
