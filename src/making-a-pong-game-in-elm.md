Title: Making a pong game in elm
Date: 2019-03-13 17:53
Category: elm
Tags: gamedev


Let's make a pong game in [elm](https://elm-lang.org/), by taking [tiny
steps](https://medium.com/@dillonkearns/moving-faster-with-tiny-steps-in-elm-2e6a269e4efc>).

If you haven't already, the very first step is to [install
elm](https://guide.elm-lang.org/install.html), and to keep in mind that the
folks on [the slack](https://elmlang.herokuapp.com/) are very friendly and
helpful if you ever face an issue that you can't manage to solve on your own.
You are not alone!


## Create the project

```shell
$ elm init
```

This creates a `elm.json` file for you, and an empty `src/` folder. Running
`elm make` will compile the project and tell you:

```shell
$ elm make
Dependencies loaded from local cache.
Dependencies ready!
-- NO INPUT --------------------------------------------------------------------

What should I make though? I need more information, like:

	elm make src/Main.elm
	elm make src/This.elm src/That.elm

However many files you give, I will create one JS file out of them.
```

Ok, so let's create a very basic `src/Main.elm` file:

```elm
module Main exposing (main)

import Html


main =
	Html.text "Hello world"
```

Running `elm make src/Main.elm` will compile successfully and create an
`index.html` file for us. Opening it in the browser displays a very dull
*Hello world* message. Dull, for sure, but still a success!

[Source code up to this point](https://github.com/magopian/elm-pong/tree/0-create-project).

## Display a ball

We're going to use the `elm/svg`, so we need to install it:

```shell
elm install elm/svg
```

Here's the result in the `elm.json` file once elm added the dependency for us:

```diff
         "direct": {
             "elm/browser": "1.0.1",
             "elm/core": "1.0.2",
-            "elm/html": "1.0.0"
+            "elm/html": "1.0.0",
+            "elm/svg": "1.0.1"
         },
         "indirect": {
             "elm/json": "1.1.3",
```

Once that's done, let's first draw a playing field (an empty light gray box),
by changing our `src/Main.elm` file to:

```elm
module Main exposing (main)

import Svg exposing (..)
import Svg.Attributes exposing (..)


main =
    svg
        [ width "500"
        , height "500"
        , viewBox "0 0 500 500"
        , Svg.Attributes.style "background: #efefef"
        ]
        [ circle
            [ cx "250"
            , cy "250"
            , r "10"
            ]
            []
        ]
```

[commit](https://github.com/magopian/elm-pong/commit/7e3dd8b0b64b8eb99f8e18105f3cf8a892e3c59c)

This display a 500px by 500px light gray rectangle, with a 10px circle right in
the center:

![the pong ball]({static}/images/elm-pong_ball.png)


Let's pull this circle out and make a `viewBall` function:

```diff
         , viewBox "0 0 500 500"
         , Svg.Attributes.style "background: #efefef"
         ]
-        [ circle
-            [ cx "250"
-            , cy "250"
-            , r "10"
-            ]
-            []
+        [ viewBall
         ]
+
+
+viewBall : Svg msg
+viewBall =
+    circle
+        [ cx "250"
+        , cy "250"
+        , r "10"
+        ]
+        []
```

[commit](https://github.com/magopian/elm-pong/commit/e4884af17d60089d38af056394e6919e8e865052)

This doesn't give us much, yet. Now what's our next tiny step? Well, to display
a ball, the function only needs its coordinates:

```diff
         , viewBox "0 0 500 500"
         , Svg.Attributes.style "background: #efefef"
         ]
-        [ viewBall
+        [ viewBall 250 250
         ]
 
 
-viewBall : Svg msg
-viewBall =
+viewBall : Int -> Int -> Svg.Svg msg
+viewBall x y =
     circle
-        [ cx "250"
-        , cy "250"
+        [ cx <| String.fromInt x
+        , cy <| String.fromInt y
         , r "10"
         ]
         []
```

[commit](https://github.com/magopian/elm-pong/commit/7146521653c54b875d1d268cc9cbef6f71b3af16)

Here we started using integers for the positions (a number of pixels), instead
of strings. This is because we will need to do some mathematics on the
position, to get the ball moving.
So we'll pass integers around, store them in our state, and at the last moment
we'll translate them back to strings.

Talking about state, let's have a `Ball` type alias for a record holding the
position:

```diff
 import Svg.Attributes exposing (..)
 
 
+type alias Ball =
+    { x : Int
+    , y : Int
+    }
+
+
+ball =
+    { x = 250
+    , y = 250
+    }
+
+
 main =
     svg
         [ width "500"
         , height "500"
         , viewBox "0 0 500 500"
         , Svg.Attributes.style "background: #efefef"
         ]
-        [ viewBall 250 250
+        [ viewBall ball
         ]
 
 
-viewBall : Int -> Int -> Svg.Svg msg
-viewBall x y =
+viewBall : Ball -> Svg.Svg msg
+viewBall { x, y } =
     circle
         [ cx <| String.fromInt x
         , cy <| String.fromInt y
```

[commit](https://github.com/magopian/elm-pong/commit/42971617722d016d7f3e944ed44028eb626c5915)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/1-display-ball).

## Move the ball

Well, the ball isn't worth much if it's not moving, so let's do that.
But let's pause for a moment, how would we achieve that?

In javascript we'd probably use `setInterval`, or `setTimeout`, and move the
ball by a small amount every 16ms or so (which would give us 60fps: 1000ms /
16ms = 62.5 frames per second).
Or we could use
[requestAnimationFrame](https://developer.mozilla.org/docs/Web/API/Window/requestAnimationFrame)
which is an even better solution.

In elm we have the
[onAnimationFrameDelta](https://package.elm-lang.org/packages/elm/browser/latest/Browser-Events#onAnimationFrameDelta)
event that we can subscribe to, which gives us the number of milliseconds
elapsed since the previous animation frame. This way we can

1. animate the ball as smoothly as possible
2. move the ball by the proper amount, computed with the elapsed time between
two frames

To subscribe to browser events we first need to change our program to be
embedded as a
[Browser.element](https://package.elm-lang.org/packages/elm/browser/latest/Browser#element).

Let's do that a tiny step at a time. First let's extract the `svg` into its own view:


```diff
 main =
+    view ball
+
+
+view : Ball -> Svg.Svg ()
+view ball_ =
     svg
         [ width "500"
         , height "500"
         , viewBox "0 0 500 500"
         , Svg.Attributes.style "background: #efefef"
         ]
-        [ viewBall ball
+        [ viewBall ball_
         ]

```

[commit](https://github.com/magopian/elm-pong/commit/f0a30bb99d11882fc8cca3e0f5dd068bd373b8bb)

Now let's actually change the `main` to be a `Browser.element`. At the top of the file:

```diff
 module Main exposing (main)
 
+import Browser
 import Svg exposing (..)
 import Svg.Attributes exposing (..)
```

And below:

```diff
     }
 
 
+main : Program () () ()
 main =
-    view ball
+    Browser.element
+        { init = \_ -> ( (), Cmd.none )
+        , view = \_ -> view ball
+        , update = \_ _ -> ( (), Cmd.none )
+        , subscriptions = \_ -> Sub.none
+        }
 
 
 view : Ball -> Svg.Svg ()
```

[commit](https://github.com/magopian/elm-pong/commit/c31bde2ad50b520f9ea9a97a0dacd56e2ddadf84)

Well, that's an awful lot of empty parens `()`. Those are of the [unit
type](https://package.elm-lang.org/packages/elm/core/latest/Basics#Never) in
elm. They are just placeholders for now, as we're going to need some model,
flags, messages...

Also, what's with all those `\_ ->`? That's how we write [anonymous
functions](https://elm-lang.org/docs/syntax#functions). And the `_` simply
means we don't care about that argument's value.

So the anonymous function provided for the element's update `\_ _ -> ( (), Cmd.none )`
can be written:

```elm
someFunction someArg someOtherArg = ( (), Cmd.none )
```

Let's start with a `Model`: this is, by convention in elm, the name of the
state, the place were we store all the data needed by our system: the ball
position, the paddles, the score, you name it. For now the only piece of data
we have is the ball position, so our model can simply be a type alias to it.

The `Model` goes near the top of the file by convention:

```diff
 import Svg.Attributes exposing (..)
 
 
+type alias Model =
+    Ball
+
+
 type alias Ball =
     { x : Int
     , y : Int
```

And the `main`:

```diff
     }
 
 
-main : Program () () ()
+main : Program () Model ()
 main =
     Browser.element
-        { init = \_ -> ( (), Cmd.none )
-        , view = \_ -> view ball
-        , update = \_ _ -> ( (), Cmd.none )
+        { init = \_ -> ( ball, Cmd.none )
+        , view = view
+        , update = \_ model -> ( model, Cmd.none )
         , subscriptions = \_ -> Sub.none
         }
 
 
-view : Ball -> Svg.Svg ()
-view ball_ =
+view : Model -> Svg.Svg ()
+view model =
     svg
         [ width "500"
         , height "500"
         , viewBox "0 0 500 500"
         , Svg.Attributes.style "background: #efefef"
         ]
-        [ viewBall ball_
+        [ viewBall model
         ]
```

[commit](https://github.com/magopian/elm-pong/commit/ab18f793ba18f2abd264c67b5b5834705c29e427)

Let's have a proper initialization function now: given some flags (none in our
case, so we'll just keep the unit for now), it generates the initial model and
commands (and we'll use
[Cmd.none](https://package.elm-lang.org/packages/elm/core/latest/Platform-Cmd#none)
for now):

```diff
     }
 
 
-ball =
-    { x = 250
-    , y = 250
-    }
+init : () -> ( Model, Cmd () )
+init _ =
+    ( { x = 250
+      , y = 250
+      }
+    , Cmd.none
+    )
 
 
 main : Program () Model ()
 main =
     Browser.element
-        { init = \_ -> ( ball, Cmd.none )
+        { init = init
         , view = view
         , update = \_ model -> ( model, Cmd.
```

[commit](https://github.com/magopian/elm-pong/commit/73bb4c464eddd603ebe53cdde4b092a9f594131e)

Ok, we should be mostly set up to receive events from the browser, and in
particular the animation frames. A few missing pieces: we need to
[subscribe](https://package.elm-lang.org/packages/elm/core/latest/Platform-Sub)
to those events, and we need to provide a message to the subscription, which
will act as a kind of callback. The elm runtime will call our (future) update
function with this message and our current model, to allow us to update the
model. This updated model will then be passed down the `view` function to
update what we see on the screen.

Let's define a `Msg` type (this is the conventional name used in elm):

```diff
     }
 
 
+type Msg
+    = OnAnimationFrame Float
+
+
 init : () -> ( Model, Cmd () )
 init _ =
     ( { x = 250
```

[commit](https://github.com/magopian/elm-pong/commit/8c560e9a5d9b0b0803cecedea4bd5b07b0336166)

This is a custom time named `OnAnimationFrame` which takes (includes?
encapsulates? boxes?) a float which is the number of milliseconds since the
previous animation frame.

We can now use this `Msg` type everywhere we used the unit previously...

In the `init` type definition:

```diff
     = OnAnimationFrame Float
 
 
-init : () -> ( Model, Cmd () )
+init : () -> ( Model, Cmd Msg )
 init _ =
     ( { x = 250
       , y = 250
```

In the `main` type definition:

```diff
     )
 
 
-main : Program () Model ()
+main : Program () Model Msg
 main =
     Browser.element
         { init = init
```

In the `view` type definition:

```diff
         }
 
 
-view : Model -> Svg.Svg ()
+view : Model -> Svg.Svg Msg
 view model =
     svg
         [ width "500"
```

And in the `viewBall` type definition:

```diff
         ]
 
 
-viewBall : Ball -> Svg.Svg msg
+viewBall : Ball -> Svg.Svg Msg
 viewBall { x, y } =
     circle
         [ cx <| String.fromInt x
```

[commit](https://github.com/magopian/elm-pong/commit/a5a6c38d8d263c02b171efe517fcf3c85477d71b)

We can now subscribe to the event.

First add the `Browser.Events` import at the top of the file:

```diff
 module Main exposing (main)
 
 import Browser
+import Browser.Events
 import Svg exposing (..)
 import Svg.Attributes exposing (..)
```

Then use a `subscriptions` function in the `main`:

```diff
         { init = init
         , view = view
         , update = \_ model -> ( model, Cmd.none )
-        , subscriptions = \_ -> Sub.none
+        , subscriptions = subscriptions
         }
```

Then add the `subscriptions` function at the bottom of the file:

```diff
         , r "10"
         ]
         []
+
+
+subscriptions : Model -> Sub Msg
+subscriptions _ =
+    Browser.Events.onAnimationFrameDelta OnAnimationFrame

```

[commit](https://github.com/magopian/elm-pong/commit/c6f34bebdb5630c2ff8dfc32aef50bef67baeb51)

If you compiled your elm files with the `--debug` option for [elm
make](https://guide.elm-lang.org/install.html#elm-make), you should see many
many messages being received in the time traveller debug window:

![OnAnimationFrame messages being listed in the time travel debugger]({static}/images/elm-pong_debug_events.png)

Let's finally add a (mostly empty) `update` function, and add a `Flags` type
alias on the unit type to clean things up a bit:

```diff
 type Msg
     = OnAnimationFrame Float
 
 
-init : () -> ( Model, Cmd Msg )
+type alias Flags =
+    ()
+
+
+init : Flags -> ( Model, Cmd Msg )
 init _ =
     ( { x = 250
       , y = 250
       }
     , Cmd.none
     )
 
 
-main : Program () Model Msg
+main : Program Flags Model Msg
 main =
     Browser.element
         { init = init
         , view = view
-        , update = \_ model -> ( model, Cmd.none )
+        , update = update
         , subscriptions = subscriptions
         }
 
 
+update : Msg -> Model -> ( Model, Cmd Msg )
+update msg model =
+    ( model, Cmd.none )
+
+
 view : Model -> Svg.Svg Msg
 view model =
     svg
```

[commit](https://github.com/magopian/elm-pong/commit/4e899ec200c65a9b4467ac21e2e753ee1e173b35)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/2-move-ball-maybe).

We can be proud of ourselves: we changed a lot of code, but nothing changed
visually: the ball still isn't moving! Promise, we're moving this ball next ;)


## Move the ball (for real)

Now that we have everything in place, moving the ball is simply a matter of
changing the `x` or `y` coordinates.
And where better to do that than on each animation frame? We already have a
subscription that fires an "event" (a message in elm's vocabulary). We also
have an `update` function that is called with those messages, allowing us to
return a new (and modified) model.

Yes, returning a new model because in elm everything is immutable: you don't
change a model, you don't mutate it, you simply create a new one:

```diff
 update : Msg -> Model -> ( Model, Cmd Msg )
 update msg model =
-    ( model, Cmd.none )
+    case msg of
+        OnAnimationFrame timeDelta ->
+            ( { model | x = model.x + 4 }, Cmd.none )
 
 
 view : Model -> Svg.Svg Msg
```

[commit](https://github.com/magopian/elm-pong/commit/065042448a7f1acedb9a66f730b8c51040c2392c)

[Source code up to this point](https://github.com/magopian/elm-pong/tree/3-move-ball).

Instead of always returning the same model we were passed in the update
function, we now add 4 pixels to the `x` coordinates of the ball.

The `{ foo | bar = crux }` notation is syntactic sugar to create a new record
from the content of the `foo` record, but with the `bar` field set to the new
`crux` value.

Once compiled and the browser tab refreshed, you should see the mighty ball
moving rather quickly towards the right (and then disappearing!).

Now that the ball is moving, let's set us up quickly with some better tooling.


## Tooling

At this point, you should start getting tired of running `elm make`, then
switching to the browser, refreshing the page... modifying the code, and then
starting over.
Those few steps can quickly become tedious, and that's why most elm developers
take advantage of:

### Live reloading

Live reloading is automatically re-compiling the code whenever a file changes,
and then automatically refreshing the browser tab.
There are a few tools available that I know of:

- [elm-live](https://github.com/wking-io/elm-live)
- [create-elm-app](https://github.com/halfzebra/create-elm-app)
- [parceljs](https://parceljs.org/elm.html)

They all offer some kind of web server that injects some javascript in the page, and then whenever a file changes, recompile the project, and communicate with the loaded web page using a websocket so it reloads.
I've used all three in various projects, and they all have their up and downs.
I find elm-live to be one of the smallest and simplest to use, but really do
feel free to pick one (but pick one, it's really worth it ;)

### Auto code formatting

Another tedious task is indenting and formatting the code properly. In elm,
indentation is matters, and as in any written code, readability is important.
The elm community has very broadly adopted a common code formatting tool that
gives us a way to all share a same code style, which is a real blessing.

It also appears that once you stop caring about a code style, and let the
machine do it for you, it really frees your mind from this chore, and removes
all the bikeshedding and useless discussions and trolls.

This code formatting tool is [elm-format](https://github.com/avh4/elm-format),
and can be configured to automatically reformat the code on save in most
editors.

With those two tools installed and set up, let us continue with our game:
adding a paddle!
