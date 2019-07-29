Title: Making a pong game in elm (2)
Date: 2019-07-26 10:31
Category: elm
Tags: gamedev


Following the [previous blog post]({filename}/making-a-pong-game-in-elm.md),
let's continue taking tiny steps in our endeavour to create a pong game in elm.

We left off with a ball and a single paddle. The ball would move towards the
right, bounce off the paddle, and then move left until it left the screen.


## Adding a left paddle

Before adding a left paddle, let's slightly change our code to prepare for it,
by renaming the current paddle to `rightPaddle`:

```diff
 type alias Model =
     { ball : Ball
-    , paddle : Paddle
+    , rightPaddle : Paddle
     }
 
 
@@ -38,9 +38,8 @@ type alias Flags =
 
 init : Flags -> ( Model, Cmd Msg )
 init _ =
-    ( { ball =
-            initBall
-      , paddle = initPaddle
+    ( { ball = initBall
+      , rightPaddle = initPaddle
       }
     , Cmd.none
     )
@@ -83,7 +82,7 @@ update msg model =
                     model.ball
 
                 shouldBounce =
-                    shouldBallBounce model.paddle model.ball
+                    shouldBallBounce model.rightPaddle model.ball
 
                 horizSpeed =
                     if shouldBounce then
@@ -109,7 +108,7 @@ shouldBallBounce paddle ball =
 
 
 view : Model -> Svg.Svg Msg
-view { ball, paddle } =
+view { ball, rightPaddle } =
     svg
         [ width "500"
         , height "500"
@@ -117,7 +116,7 @@ view { ball, paddle } =
         , Svg.Attributes.style "background: #efefef"
         ]
         [ viewBall ball
-        , viewPaddle paddle
+        , viewPaddle rightPaddle
         ]
```

[commit](https://github.com/magopian/elm-pong/commit/f8d33e5916ffc1445003e0d3c2df6c9efb6e9d0b)

Adding the left paddle should now be very straightforward:

```diff
 type alias Model =
     { ball : Ball
     , rightPaddle : Paddle
+    , leftPaddle : Paddle
     }
 
 
@@ -40,6 +41,7 @@ init : Flags -> ( Model, Cmd Msg )
 init _ =
     ( { ball = initBall
       , rightPaddle = initPaddle
+      , leftPaddle = initPaddle
       }
     , Cmd.none
     )
@@ -108,7 +110,7 @@ shouldBallBounce paddle ball =
 
 
 view : Model -> Svg.Svg Msg
-view { ball, rightPaddle } =
+view { ball, rightPaddle, leftPaddle } =
     svg
         [ width "500"
         , height "500"
@@ -117,6 +119,7 @@ view { ball, rightPaddle } =
         ]
         [ viewBall ball
         , viewPaddle rightPaddle
+        , viewPaddle leftPaddle
         ]
```

[commit](https://github.com/magopian/elm-pong/commit/82706931c5682434fb638b0cd94004e46af03311)

Yes, you clever person, I know what you're thinking: "we can't see the left
paddle! And it's obvious, it's because you placed it exactly at the same
position as the right paddle!". I'm proud of you, and yes, you are right.
Let's fix that by modifying the `initPaddle` function which should now take an
initial `x` position.

```diff
 init : Flags -> ( Model, Cmd Msg )
 init _ =
     ( { ball = initBall
-      , rightPaddle = initPaddle
-      , leftPaddle = initPaddle
+      , rightPaddle = initPaddle 480
+      , leftPaddle = initPaddle 10
       }
     , Cmd.none
     )
@@ -56,9 +56,9 @@ initBall =
     }
 
 
-initPaddle : Paddle
-initPaddle =
-    { x = 480
+initPaddle : Int -> Paddle
+initPaddle initialX =
+    { x = initialX
     , y = 225
     , width = 10
     , height = 50
```

[commit](https://github.com/magopian/elm-pong/commit/3bb0e3e519785f12741c398d73315ffc57da0ef1)

![Left paddle with the ball moving towards it]({static}/images/elm-pong_left_paddle.png)

"But wait Mathieu, can't you see the ball is going right through the left
paddle!". I sure do, and yes, let's now fix that by changing the
`shouldBallBounce` helper function.

It'll be a bit tricky though, because we need to check both paddles slightly
differently: if it's the left paddle, the check on the `y` position is exactly
the same, but the check on the `x` position now needs to make sure that the
ball stays "right of" the left paddle. And so that the ball's center minus its
radius is higher than the left paddle's `x` position plus its width.

```diff
                 shouldBounce =
                     shouldBallBounce model.rightPaddle model.ball
+                        || shouldBallBounce model.leftPaddle model.ball
 
                 horizSpeed =
                     if shouldBounce then
@@ -104,9 +105,17 @@ update msg model =
 
 shouldBallBounce : Paddle -> Ball -> Bool
 shouldBallBounce paddle ball =
-    (ball.x + ball.radius >= paddle.x)
-        && (ball.y >= paddle.y)
-        && (ball.y <= paddle.y + 50)
+    if paddle.x == 10 then
+        -- left paddle
+        (ball.x - ball.radius <= paddle.x + paddle.width)
+            && (ball.y >= paddle.y)
+            && (ball.y <= paddle.y + 50)
+
+    else
+        -- right paddle
+        (ball.x + ball.radius >= paddle.x)
+            && (ball.y >= paddle.y)
+            && (ball.y <= paddle.y + 50)
```

[commit](https://github.com/magopian/elm-pong/commit/4be1df966bd9350ffbd8718896c2157345e47847)

It's now working exactly as expected:

![Ball bouncing between the right and left paddle]({static}/images/elm-pong_bouncing_ball.gif)

That's a huge success, let's take a pause, and reflect on our awesomeness.
