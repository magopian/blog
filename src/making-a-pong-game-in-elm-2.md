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

That's a huge success, let's take a pause, and reflect on our awesomeness!


## Refactoring and types

If you're like me, you feel that there's something smelly. Something fishy.
Something that isn't quite right.

I mean, what's with the `shouldBallBounce` function, and its check on the
paddle's `x` position? Sure, there's a comment in there, which is a bit like a
perfume spread on something smelly: it doesn't make the smelly thing less
smelly, it just kinda hides the smell.
And I've written "smell" way to often in the last couple sentences (see the
[code smell definition](https://en.wikipedia.org/wiki/Code_smell) for the
reference).

Instead of checking the `x` position of a paddle to know if it's the left or the right one, it would be very useful to declare the paddles as `left` or `right`.

In other languages, people would use something like an `enum`, but in elm,
there's a wonderful thing called
[custom types](https://guide.elm-lang.org/types/custom_types.html) which are
very powerful and convenient to use:

```elm
type Paddle
    = LeftPaddle
    | RightPaddle
```

Actually, we need the rendering information (`x`, `y`, `width`, `height`) for each paddle, so it should rather be something like:

```elm
type Paddle
    = LeftPaddle { x: Int, y: Int, width: Int, height: Int}
    | RightPaddle { x: Int, y: Int, width: Int, height: Int}
```

By now, this thing might ring a bell to you: in the previous installment we
declared another custom type (the `Msg`) which also encapsulated some data.
It did ring a bell to you, didn't it? You're clever, and I'm proud of you. You
should also be proud of yourself. And even if it didn't ring a bell to you, I'm
sure it'll will in the future, and I'm proud of you all the same!

So what are those custom types? It might be one of the features of elm that I
find the most difficult to put in words, even though they feel so natural now
that I'm used to them.

They're composed of:

- a name: the type itself (`Msg`, `Paddle`, ...)
- some variants: you can see those as functions, or constructors. They are the
  different "values" for this type. For the `Msg` type we only declared one. For
  the `Paddle` type we'll have two (`LeftPaddle` and `RightPaddle`).
- some optional data attached to those variants: the `OnAnimationFrame` variant
  had a float, our `LeftPaddle` and `RightPaddle` have some rendering
  information.

Regarding the optional data attached, you can have variants with and without
those. This is how you could type an answer which is either yes, no, or
other with some additional information.

```elm
type Answer
    = Yes
    | No
    | Other String
```

And here, `String` is just a type, so it could be a custom type of our own, or
a `type alias` like so:

```elm
type alias Reason = String

type Answer
    = Yes
    | No
    | Other Reason
```

In this example, using a type alias is a nice way to document the code and make
it more understandable.

Oh, and cool thing, a variant can have any number of data attached to it, so we
could imagine having

```elm
type Paddle
    = LeftPaddle Int Int Int Int
    | RightPaddle Int Int Int Int
```

But then we'd have to remember which `Int` is for which type of data, which
would be unconvenient, more difficult to maintain, and generally seen as bad
practice.

Soooooo, after all this chatter, let's

- declare a `PaddleInfo` type alias to hold all the rendering data
- attach this `PaddleInfo` to the modified `Paddle` type variants

```diff
-type alias Paddle =
+type Paddle
+    = RightPaddle PaddleInfo
+    | LeftPaddle PaddleInfo
+
+
+type alias PaddleInfo =
     { x : Int
     , y : Int
     , width : Int
     , height: Int
     }
```

And now for arguably the best part of elm: the compiler. Let's compile this,
and follow the errors that the compiler is giving us, and we'll have everything
compiling and working again in a jiffy.

The first error says:

```shell
-- TYPE MISMATCH -------------------------------------------------- src/Main.elm

Something is off with the body of the `initPaddle` definition:

66|>    { x = initialX
67|>    , y = 225
68|>    , width = 10
69|>    , height = 50
70|>    }

The body is a record of type:

    { height : number, width : number1, x : Int, y : number2 }

But the type annotation on `initPaddle` says it should be:

    Paddle
```

Here, the compiler complains because we changed to the `Paddle` type, and the
`initPaddle` function signature still says it's returning a `Paddle`, but it
should instead be a `PaddleInfo`:

```diff
-initPaddle : Int -> Paddle
+initPaddle : Int -> PaddleInfo
 initPaddle initialX =
     { x = initialX
     , y = 225
```

The next compiler error is:

```shell
-- TYPE MISMATCH -------------------------------------------------- src/Main.elm

Something is off with the body of the `init` definition:

47|>    ( { ball = initBall
48|>      , rightPaddle = initPaddle 480
49|>      , leftPaddle = initPaddle 10
50|>      }
51|>    , Cmd.none
52|>    )

The body is a tuple of type:

    ( { ball : Ball, leftPaddle : PaddleInfo, rightPaddle : PaddleInfo }
    , Cmd msg
    )

But the type annotation on `init` says it should be:

    ( Model, Cmd Msg )
```

What this says is that the `init` function should return a `( Model, Cmd Msg )`
but it returns something else instead of the `Model`: a record that has two
fields `rightPaddle` and `leftPaddle` that are... `PaddleInfo` (instead of
`Paddle`). Let's change this:

```diff
 init : Flags -> ( Model, Cmd Msg )
 init _ =
     ( { ball = initBall
-      , rightPaddle = initPaddle 480
-      , leftPaddle = initPaddle 10
+      , rightPaddle = RightPaddle <| initPaddle 480
+      , leftPaddle = LeftPaddle <| initPaddle 10
       }
     , Cmd.none
     )
```

As a refresher, the `<|` syntactic sugar means that we're taking the result of
what's on the right of the "arrow", and using it as an argument for what's on
the left. So we're using the `PaddleInfo` we're getting back from the
`initPaddle` helper function, and "attaching" it to the `Paddle` variant.
This could also be rewritten `RightPaddle (initPaddle 480)`.

The next error is:

```shell
-- TYPE MISMATCH -------------------------------------------------- src/Main.elm

This is not a record, so it has no fields to access!

113|     if paddle.x == 10 then
            ^^^^^^
This `paddle` value is a:

    Paddle

But I need a record with a x field!
```

This is interesting: the line `113` is in the `shouldBallBounce` function,
which is where we started all this refactoring. We're now ready to reap the
benefits:

```diff
 shouldBallBounce : Paddle -> Ball -> Bool
 shouldBallBounce paddle ball =
-    if paddle.x == 10 then
-        -- left paddle
-        (ball.x - ball.radius <= paddle.x + paddle.width)
-            && (ball.y >= paddle.y)
-            && (ball.y <= paddle.y + 50)
-
-    else
-        -- right paddle
-        (ball.x + ball.radius >= paddle.x)
-            && (ball.y >= paddle.y)
-            && (ball.y <= paddle.y + 50)
+    case paddle of
+        LeftPaddle { x, y, width, height } ->
+            (ball.x - ball.radius <= x + width)
+                && (ball.y >= y)
+                && (ball.y <= y + height)
+
+        RightPaddle { x, y, height } ->
+            (ball.x + ball.radius >= x)
+                && (ball.y >= y)
+                && (ball.y <= y + height)
```

"MATHIEU?! WHAT KIND OF VOODOO IS THAT YOU TRICKED ME! I thought this was going
to be an easy to follow guide, and now I feel miserable!"

I'm sorry, please bear with me for a minute while I dissect what happened here:

- we already saw the `case` in the previous blog post when writing the `update`
  function. It's like a `switch` in some other languages, and it's used to
  "select" which branch of code to execute given what the "shape" of the data
  is. Here we're selecting based on the variants of `Paddle` (`LeftPaddle` or
  `RightPaddle`).
- the `case` also allows us to
  ["destructure" or "pattern match"](https://gist.github.com/yang-wei/4f563fbf81ff843e8b1e)
  the type and its attached data. What we're saying is "if there's a
  `LeftPaddle` then assign its `x`, `y`, `width` and `height` to variables of
  the same name. So in the code after the `->` the names `x`, `y`, ... all have
  the value of what's in the `PaddleInfo` record attached to the `Paddle` type.
- in the case of the `RightPaddle` we didn't need the `width` value, so we
  simply didn't "destructure" (and assign) it

This new code might not be much shorter, but it's way more readable, and
doesn't involve a `paddle.x` check against a hard coded value that we might
want to change in the future. Also no more need for the comments, as it's self
commenting.

And we're left with one last error:

```shell
-- TYPE MISMATCH -------------------------------------------------- src/Main.elm

This is not a record, so it has no fields to access!

152|         [ x <| String.fromInt paddle.x
                                   ^^^^^^
This `paddle` value is a:

    Paddle

But I need a record with a x field!
```

The fix is then:

```diff
 viewPaddle : Paddle -> Svg.Svg Msg
 viewPaddle paddle =
+    let
+        paddleInfo =
+            case paddle of
+                LeftPaddle info ->
+                    info
+
+                RightPaddle info ->
+                    info
+    in
     rect
-        [ x <| String.fromInt paddle.x
-        , y <| String.fromInt paddle.y
-        , width <| String.fromInt paddle.width
-        , height <| String.fromInt paddle.height
+        [ x <| String.fromInt paddleInfo.x
+        , y <| String.fromInt paddleInfo.y
+        , width <| String.fromInt paddleInfo.width
+        , height <| String.fromInt paddleInfo.height
         ]
         []
```

"MATHIEU?! YOU DID IT AGAIN!". Ok, sorry, sorry, I was being cheeky here.

The main part is this one:

```elm
    let
        paddleInfo =
            case paddle of
                LeftPaddle info ->
                    info

                RightPaddle info ->
                    info
    in
```

The `let..in` is where we assign values to names (to "variables"). Here we're
assigning the attached data of the `LeftPaddle` or `RightPaddle` to the name
`paddleInfo` (which we're using in the rest of the function code).
And we're once again using a `case` to destructure the type. Both cases are the
same (because in our case both variants of the `Paddle` custom type have a
single attached data of type `PaddleInfo`, but it could be different: as we
explained earlier, we can mix and match any kind of variants for a given custom
type).

So when we write `LeftPaddle info -> info` we're saying "if it's a `LeftPaddle`
then take its attached data and assign it to the name "info", then return this
"info" value" (and assign it to the `paddleInfo` name).

And we're now done! We have the exact same behavior, but a code that's more
precise and maintainable. I agree that it might look more complex, or sometimes
longer, but it gives us more flexibility, and above all, much better help and
guards from the compiler, which is invaluable.

[commit](https://github.com/magopian/elm-pong/commit/a3b0997e911837730e50854e0193e616945b8b53)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/6-two-paddles).
