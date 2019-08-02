Title: Making a pong game in elm (2)
Date: 2019-07-30 15:41
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
ball stays "right of" the left paddle, which means that the ball's center minus
its radius is bigger than the left paddle's `x` position plus its width.

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

I mean, what's with the `shouldBallBounce` function and its check on the
paddle's `x` position? Sure, there's a comment in there, which is a bit like a
perfume spread on something smelly: it doesn't make the smelly thing less
smelly, it just kinda hides the smell.
And I've written "smell" way too often in the last couple sentences (see the
[code smell definition](https://en.wikipedia.org/wiki/Code_smell) for the
reference).

Instead of checking the `x` position of a paddle to know if it's the left or
the right one, it would be very useful to declare the paddles as `left` or
`right`.

In other languages, people would use something like an `enum`, but in elm,
there's a wonderful thing called
[custom types](https://guide.elm-lang.org/types/custom_types.html) which are
very powerful and convenient to use:

```elm
type Paddle
    = LeftPaddle
    | RightPaddle
```

Actually, we need the position information (`x`, `y`, `width`, `height`) for
each paddle, so it should rather be something like:

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
  had a float, our `LeftPaddle` and `RightPaddle` have some position
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

Here we used the built-in String type for the associated information, but we
can use any type, including one we've defined ourselves

Oh, another cool thing, a variant can have any number of data attached to it,
so we could imagine having

```elm
type Paddle
    = LeftPaddle Int Int Int Int
    | RightPaddle Int Int Int Int
```

But then we'd have to remember which `Int` is for which type of data, which
would be inconvenient, more difficult to maintain, and generally seen as bad
practice.

Soooooo, after all this chatter, let's

- declare a `PaddleInfo` type alias to hold all the position data
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
This could also be rewritten

```elm
RightPaddle (initPaddle 480)
```

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

"MATHIEU?! WHAT KIND OF VOODOO IS THAT, YOU TRICKED ME! I thought this was going
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
same because in our case both variants of the `Paddle` custom type have a
single attached data of type `PaddleInfo`, but it could be different: as we
explained earlier, we can mix and match any kind of variants for a given custom
type.

So when we write `LeftPaddle info -> info` we're saying "if it's a `LeftPaddle`
then take its attached data and assign it to the name "info", then return this
"info" value" (which we then assign to the `paddleInfo` name in the `let..in`
clause).

And we're now done! We have the exact same behavior, but a code that's more
precise and maintainable. I agree that it might look more complex, or sometimes
longer, but it gives us more flexibility, and above all, much better help and
guards from the compiler, which is invaluable.

[commit](https://github.com/magopian/elm-pong/commit/a3b0997e911837730e50854e0193e616945b8b53)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/6-two-paddles).


## Moving the paddle

What good is a game if the player has no control whatsoever on it? It's high
time that we give a way for the player to move the paddle. We'll start with the
right paddle, just because.

This can't be hard, right? RIGHT? WRONG!

Sometimes elm feel complex. Complicated. Overengineered. Hard. Difficult. And
that is because it's trying to do the right thing, not the simple thing. It's
trying very very hard to prevent you from shooting yourself in the foot. It's
helping you not have any runtime errors.

One such case are
[JSON decoders](https://guide.elm-lang.org/effects/json.html). And those are
probably one of the major hurdles that elm beginners will face at some point,
and feel overwhelmed.


### Why decoders?

If they are so difficult, why bother at all? I mean, JSON is easy, right?
Strings, bools, arrays, objects, numbers... how hard can it be?

Let's take a step back for a moment: if the elm compiler is going to help you
have no runtime exception, it needs to be able to guarantee that there's no bad
code branches. That a given field in the JSON object you're getting back is
indeed a number, and not a string, or an array, or a null. Because if it can't
guarantee that a value is of the proper type, it can't guarantee that the
operations you do on that value are valid.

So, if the elm compiler needs to know the type of the fields in the JSON it
gets, it needs a way to "decode" this JSON into proper types. And if the JSON
doesn't decode properly into those types, then it'll fail in an expected way,
and make you write a code branch for that case, so it doesn't end blowing up in
your face at runtime.

That's where and why decoders are useful: you provide a "translation" from a
untyped JSON to a typed value: if it succeeds, then you can use that typed
value. If it fails, you handle this case (by displaying an error message for
example).

You can see that as a way to validate the JSON that elm is receiving from the
javascript land in the case of an event, or from an http request to a remote
API.

So yes, decoders are hard to grasp. But if you trust my own experience, once
you get to use them, you'll be missing them in other languages, and hoping
there was a way to achieve the same result.


### Keyboard events

There's a convenient
[Browser.Event module](https://package.elm-lang.org/packages/elm/browser/latest/Browser-Events#keyboard)
that provides event listeners for keyboard events.

Remember when we subscribed to the `Browser.Events.onAnimationFrameDelta`
events in the previous episode? We'll do basically the same this time around.

We need to do a few things:

- Decode a `String` from the keydown event
- Attach that string to a `Msg` variant that we'll add: `KeyDown String`, so
  the decoder returns a `Decoder Msg`
- Provide that decoder to the
  [Browser.Events.onKeyDown](https://package.elm-lang.org/packages/elm/browser/latest/Browser-Events#onKeyDown)
  subscription
- Add a branch to the `case` in the `update` function to deal with the new
  `Msg` variant (we'll only display some debug info in the console for now)
- Add an import to the `Json.Decode` module

```diff
 import Browser
 import Browser.Events
+import Json.Decode as Decode
 import Svg exposing (..)
 import Svg.Attributes exposing (..)
 
@@ -36,6 +37,7 @@ type alias PaddleInfo =
 
 type Msg
     = OnAnimationFrame Float
+    | KeyDown String
 
 
 type alias Flags =
@@ -107,6 +109,13 @@ update msg model =
             in
             ( { model | ball = updatedBall }, Cmd.none )
 
+        KeyDown keyString ->
+            let
+                _ =
+                    Debug.log "key pressed" keyString
+            in
+            ( model, Cmd.none )
+
 
 shouldBallBounce : Paddle -> Ball -> Bool
 shouldBallBounce paddle ball =
@@ -168,4 +177,12 @@ viewPaddle paddle =
 
 subscriptions : Model -> Sub Msg
 subscriptions _ =
-    Browser.Events.onAnimationFrameDelta OnAnimationFrame
+    Sub.batch
+        [ Browser.Events.onAnimationFrameDelta OnAnimationFrame
+        , Browser.Events.onKeyDown (Decode.map KeyDown keyDecoder)
+        ]
+
+
+keyDecoder : Decode.Decoder String
+keyDecoder =
+    Decode.field "key" Decode.string
```

[commit](https://github.com/magopian/elm-pong/commit/8555850f4eb96cc781eb0bd512a5415cb4663168)

We used `Decode.map` here to attach the string we get back from the decoder to
the `KeyDown` variant... but only if the `keyDecoder` succeeded!

`Decode.map` says "if the decoder succeeds, apply this function to the result".
And we needed to do that because the `onKeyDown` event listener needs a
`Decoder Msg` and not a `Decoder String`. In order to be able to subscribe to
the events, the listener needs to know which message to call when it receives
an event.

If you followed along, you'll notice a compiler error:

```shell
-- UNKNOWN IMPORT ------------------------------------------------- src/Main.elm

The Main module has a bad import:

    import Json.Decode

Do you want the one from the elm/json package? If so, run this command to add
that dependency to your elm.json file:

    elm install elm/json

If you want a local file, make sure the `Json.Decode` module is in one of the
"source-directories" listed in your elm.json file.
```

This very helpful message tells us that we need to add the missing dependency
to the `elm.json` file, just like we did with `elm/svg` in the previous post.
Running the `elm install elm/json` command result in the following changes in
the `elm.json` file:

```diff
             "elm/browser": "1.0.1",
             "elm/core": "1.0.2",
             "elm/html": "1.0.0",
+            "elm/json": "1.1.3",
             "elm/svg": "1.0.1"
         },
         "indirect": {
-            "elm/json": "1.1.3",
             "elm/time": "1.0.0",
             "elm/url": "1.0.0",
             "elm/virtual-dom": "1.0.2"
```

It moved the `elm/json` dependency from the indirect dependencies to the
direct ones.

In the previous post we already used the `Debug.log` helper, so let's take a
minute to explain what that does: it's a function takes any argument (in our
case the `keyString`) and displays it in the browser console, preceeded by the
message you provide it (eg `key pressed`).

This is the result of pressing a few keys in the console:

![Debug.log messages in the console]({static}/images/elm-pong_debug_log.png)

The `Debug.log` helper also returns exactly what it received, so you can add it
anywhere, it's very convenient!

However, be aware that it's not possible to use the elm compiler optimization
with a `Debug.xxx` call, so they need to be removed before you compile for
production.

In our case, we wanted to output a debug message to the console, but not do
anything else. A common pattern is to use a `let..in` to fake a variable
assignment, but not care about the resulting variable (hence the `_ = ...`). As
we're not doing anything with the keyboard event (yet), we're also returning
the exact same model we received in the update function, and send no commands:
`( model, Cmd.none)`.


### Decoding arrow key presses

There's a very convenient link in the `onKeyDown` documentation that
brings us straight to something of great interest to us: [Decoding for
games](https://github.com/elm/browser/blob/1.0.0/notes/keyboard.md#decoding-for-games).

As explained, it would make a lot of sense and give us some guarantees to use
a custom type (that we could call `PlayerAction`):

```diff
 type Msg
     = OnAnimationFrame Float
-    | KeyDown String
+    | KeyDown PlayerAction
+
+
+type PlayerAction
+    = RightPaddleUp
+    | RightPaddleDown
```

Notice here that we didn't add an `Other` variant, because we'll be doing
something else with the decoder... Event listeners in elm have a nice (and
sometimes confusing?) behavior: whenever the decoder that they're given fails
decoding, the event is simply discarded. Which means that no `Msg` is sent.
It's as if the program simply didn't subscribe to those.

So we're going to modify our decoder to pass the resulting decoded string to
another decoder using the `Decode.andThen` helper. And from this second
decoder, we're going to `Decode.succeed` with one of the `PlayerAction`
variants, or `Decode.fail`, in which case the event will be discarded.

```diff
-keyDecoder : Decode.Decoder String
+keyDecoder : Decode.Decoder PlayerAction
 keyDecoder =
     Decode.field "key" Decode.string
+        |> Decode.andThen keyToPlayerAction
+
+
+keyToPlayerAction : String -> Decode.Decoder PlayerAction
+keyToPlayerAction keyString =
+    case keyString of
+        "ArrowUp" ->
+            Decode.succeed RightPaddleUp
+
+        "ArrowDown" ->
+            Decode.succeed RightPaddleDown
+
+        _ ->
+            Decode.fail "not an event we care about"
```

[commit](https://github.com/magopian/elm-pong/commit/2d859d34f8b2ac2417bfa2b5eb60fe716220bafc)

`Decode.andThen` is a bit different than `Decoder.map`: it also takes the
result of a successful decoder, but returns a decoder (not a result). Which
means that we can modify a decoder's behavior and make it fail or succeed
instead of just modifying its successful result. In our case we make it fail if
it's not one of the keys we're interested in... even though the `keyDecoder`
would successfully decode a string from the event.

Neat, isn't it? Are you starting to like decoders? Love them even? I do.


### Moving the right paddle

Now that we can detect player actions, we can react to them, and update the
paddle position:

```diff
-        KeyDown keyString ->
-            let
-                _ =
-                    Debug.log "key pressed" keyString
-            in
-            ( model, Cmd.none )
+        KeyDown playerAction ->
+            case playerAction of
+                RightPaddleUp ->
+                    ( { model | rightPaddle = model.rightPaddle |> updatePaddle -10 }
+                    , Cmd.none
+                    )
+
+                RightPaddleDown ->
+                    ( { model | rightPaddle = model.rightPaddle |> updatePaddle 10 }
+                    , Cmd.none
+                    )
+
+
+updatePaddle : Int -> Paddle -> Paddle
+updatePaddle amount paddle =
+    case paddle of
+        RightPaddle paddleInfo ->
+            { paddleInfo | y = paddleInfo.y + amount }
+                |> RightPaddle
+
+        LeftPaddle paddleInfo ->
+            { paddleInfo | y = paddleInfo.y + amount }
+                |> LeftPaddle
```

[commit](https://github.com/magopian/elm-pong/commit/94aaa6e68f964635da982a9ca03cd9ad406fcd9a)

As you can see, we used a small helper function `updatePaddle` to update the
info of a paddle, moving it up or down by a certain amount of pixels.


### Moving the left paddle

Now that we have everything in place for the right player, it's straightforward
to deal with the left player. We'll use the keys "e" for up, and "d" for down
to cope with both azerty and qwerty keyboards. I'm sorry if this doesn't make
sense for your keyboard, but I'm sure you'll be able to fix it by changing
those keys in your code ;)

Let's do that step by step with the help from the lovely compiler:

```diff
 type PlayerAction
     = RightPaddleUp
     | RightPaddleDown
+    | LeftPaddleUp
+    | LeftPaddleDown
```

We have one compiler error:

```shell
-- MISSING PATTERNS ----------------------------------------------- src/Main.elm

This `case` does not have branches for all possibilities:

120|>            case playerAction of
121|>                RightPaddleUp ->
122|>                    ( { model | rightPaddle = model.rightPaddle |> updatePaddle -10 }
123|>                    , Cmd.none
124|>                    )
125|>
126|>                RightPaddleDown ->
127|>                    ( { model | rightPaddle = model.rightPaddle |> updatePaddle 10 }
128|>                    , Cmd.none
129|>                    )

Missing possibilities include:

    LeftPaddleUp
    LeftPaddleDown

I would have to crash if I saw one of those. Add branches for them!

Hint: If you want to write the code for each branch later, use `Debug.todo` as a
placeholder. Read <https://elm-lang.org/0.19.0/missing-patterns> for more
guidance on this workflow.
```

That's an easy one:

```diff
                     , Cmd.none
                     )
 
+                LeftPaddleUp ->
+                    ( { model | leftPaddle = model.leftPaddle |> updatePaddle -10 }
+                    , Cmd.none
+                    )
+
+                LeftPaddleDown ->
+                    ( { model | leftPaddle = model.leftPaddle |> updatePaddle 10 }
+                    , Cmd.none
+                    )
+
 
 updatePaddle : Int -> Paddle -> Paddle
 updatePaddle amount paddle =
```

The thing is, once we fixed that the compiler compiles successfully... but
pressing the "e" or "d" keys has no effect whatsoever... elm compiler, why
have you failed me!!!!!

Remember when we talked about the (sometimes confusing) behavior of event
listeners in elm that are silently ignored if the decoder fails? And remember
that we used that to our advantage to reduce the code a bit instead of dealing
with an `Other` variant for the `PlayerAction` custom type?

Well here we are now: it's up to us to remember that we need to update the
decoder:

```diff
         "ArrowDown" ->
             Decode.succeed RightPaddleDown
 
+        "e" ->
+            Decode.succeed LeftPaddleUp
+
+        "d" ->
+            Decode.succeed LeftPaddleDown
+
         _ ->
             Decode.fail "not an event we care about"
```

[commit](https://github.com/magopian/elm-pong/commit/67935ae0c9fd2296103d8f0f9511d7d29fd2e0b8)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/7-move-paddles).

Well, it seems we have a mostly working pong game. Both players can move their
paddles up or down. We would still have a LOOOOOONG way to go to make it a
real, playable and enjoyable game though.

We did 80% of the work in 20% of the time. We now need 80% of the time to
finish the remaining 20% of the work ;)

Some of the things that are blatantly missing:

- losing/winning/scoring: when the ball moves off the screen the player should lose,
  and the other one should score a point
- clamping the paddles to the screen, instead of letting them wander off
- better input management: at the moment, both players can't keep pressing the
  keys at the same time, one takes precedence over the other one (at least for
  me on Firefox OSX)

Some ideas to make it more enjoyable:

- deal with acceleration of the paddle
- power ups/downs
- visual effects
- sound effects
- increasing the difficulty (faster moving ball for example, shorter paddles)
- one player mode against the computer
- move the paddle using the mouse instead of the keyboard for a smoother
  experience
- being able to play on a mobile phone/tablet using gestures
- twists on the original concept

So what did you think? Did this give you a feel for the elm language? Did it
make you want to give it a go for gamedev or webdev?

I would be curious to see if you come up with completed/improved games of your
own!

----

There's now a [follow up]({filename}/making-a-pong-game-in-elm-3.md).
