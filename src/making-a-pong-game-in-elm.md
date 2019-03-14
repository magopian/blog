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


## Display a ball

We're going to use the `elm/svg`, so we need to install it:

```shell
elm install elm/svg
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

What that does is display a 500px by 500px light gray rectangle, with a 10px
circle right in the center:

![the pong ball]({static}/images/elm-pong_ball.png)


Let's pull this circle out and make a `viewBall` function:

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
        [ viewBall
        ]


viewBall : Svg msg
viewBall =
    circle
        [ cx "250"
        , cy "250"
        , r "10"
        ]
        []
```

This doesn't give us much, yet. Now what's our next tiny step? Well, to display
a ball, the function only needs its coordinates:

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
        [ viewBall 250 250
        ]


viewBall : Int -> Int -> Svg.Svg msg
viewBall x y =
    circle
        [ cx <| String.fromInt x
        , cy <| String.fromInt y
        , r "10"
        ]
        []
```

Here we started using integers for the positions (a number of pixels), instead
of strings. This is because we will need to do some mathematics on the
position, to get the ball moving.
So we'll pass integers around, store them in our state, and at the last moment
we'll translate them back to strings.

Talking about state, let's have a `Ball` type alias for a record holding the
position:

```elm
type alias Ball =
    { x : Int
    , y : Int
    }


ball =
    { x = 250
    , y = 250
    }


main =
    svg
        [ width "500"
        , height "500"
        , viewBox "0 0 500 500"
        , Svg.Attributes.style "background: #efefef"
        ]
        [ viewBall ball
        ]


viewBall : Ball -> Svg.Svg msg
viewBall { x, y } =
    circle
        [ cx <| String.fromInt x
        , cy <| String.fromInt y
        , r "10"
        ]
        []
```


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


```elm
module Main exposing (main)

import Svg exposing (..)
import Svg.Attributes exposing (..)


type alias Ball =
    { x : Int
    , y : Int
    }


ball =
    { x = 250
    , y = 250
    }


main =
    view ball


view : Ball -> Svg.Svg ()
view ball_ =
    svg
        [ width "500"
        , height "500"
        , viewBox "0 0 500 500"
        , Svg.Attributes.style "background: #efefef"
        ]
        [ viewBall ball_
        ]


viewBall : Ball -> Svg.Svg msg
viewBall { x, y } =
    circle
        [ cx <| String.fromInt x
        , cy <| String.fromInt y
        , r "10"
        ]
        []
```

Now let's actually change the `main` to be a `Browser.element`:

```elm
module Main exposing (main)

import Browser
import Svg exposing (..)
import Svg.Attributes exposing (..)


type alias Ball =
    { x : Int
    , y : Int
    }


ball =
    { x = 250
    , y = 250
    }


main : Program () () ()
main =
    Browser.element
        { init = \_ -> ( (), Cmd.none )
        , view = \_ -> view ball
        , update = \_ _ -> ( (), Cmd.none )
        , subscriptions = \_ -> Sub.none
        }


view : Ball -> Svg.Svg ()
view ball_ =
    svg
        [ width "500"
        , height "500"
        , viewBox "0 0 500 500"
        , Svg.Attributes.style "background: #efefef"
        ]
        [ viewBall ball_
        ]


viewBall : Ball -> Svg.Svg msg
viewBall { x, y } =
    circle
        [ cx <| String.fromInt x
        , cy <| String.fromInt y
        , r "10"
        ]
        []
```

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

```elm
module Main exposing (main)

import Browser
import Svg exposing (..)
import Svg.Attributes exposing (..)


type alias Model =
    Ball


type alias Ball =
    { x : Int
    , y : Int
    }


ball =
    { x = 250
    , y = 250
    }


main : Program () Model ()
main =
    Browser.element
        { init = \_ -> ( ball, Cmd.none )
        , view = view
        , update = \_ model -> ( model, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }


view : Model -> Svg.Svg ()
view model =
    svg
        [ width "500"
        , height "500"
        , viewBox "0 0 500 500"
        , Svg.Attributes.style "background: #efefef"
        ]
        [ viewBall model
        ]


viewBall : Ball -> Svg.Svg msg
viewBall { x, y } =
    circle
        [ cx <| String.fromInt x
        , cy <| String.fromInt y
        , r "10"
        ]
        []
```

Let's have a proper initialization function now: given some flags (none in our
case, so we'll just keep the unit for now), it generates the initial model and
commands (and we'll use
[Cmd.none](https://package.elm-lang.org/packages/elm/core/latest/Platform-Cmd#none)
for now):

```elm
module Main exposing (main)

import Browser
import Svg exposing (..)
import Svg.Attributes exposing (..)


type alias Model =
    Ball


type alias Ball =
    { x : Int
    , y : Int
    }


init : () -> ( Model, Cmd () )
init _ =
    ( { x = 250
      , y = 250
      }
    , Cmd.none
    )


main : Program () Model ()
main =
    Browser.element
        { init = init
        , view = view
        , update = \_ model -> ( model, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }


view : Model -> Svg.Svg ()
view model =
    svg
        [ width "500"
        , height "500"
        , viewBox "0 0 500 500"
        , Svg.Attributes.style "background: #efefef"
        ]
        [ viewBall model
        ]


viewBall : Ball -> Svg.Svg msg
viewBall { x, y } =
    circle
        [ cx <| String.fromInt x
        , cy <| String.fromInt y
        , r "10"
        ]
        []
```

Ok, we should be mostly set up to receive events from the browser, and in
particular the animation frames. A few missing pieces: we need to
[subscribe](https://package.elm-lang.org/packages/elm/core/latest/Platform-Sub)
to those events, and we need to provide a message to the subscription, which
will act as a kind of callback. The elm runtime will call our (future) update
function with this message and our current model, to allow us to update the
model. This updated model will then be passed down the `view` function to
update what we see on the screen.

Let's define a `Msg` type (this is the conventional name used in elm):

```elm
type Msg = OnAnimationFrame Float
```

This is a custom time named `OnAnimationFrame` which takes (includes?
encapsulates? boxes?) a float which is the number of milliseconds since the
previous animation frame.

We can now use this `Msg` type everywhere we used the unit previously:

```elm
module Main exposing (main)

import Browser
import Svg exposing (..)
import Svg.Attributes exposing (..)


type alias Model =
    Ball


type alias Ball =
    { x : Int
    , y : Int
    }


init : () -> ( Model, Cmd Msg )
init _ =
    ( { x = 250
      , y = 250
      }
    , Cmd.none
    )


type Msg
    = OnAnimationFrame Float


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , view = view
        , update = \_ model -> ( model, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }


view : Model -> Svg.Svg Msg
view model =
    svg
        [ width "500"
        , height "500"
        , viewBox "0 0 500 500"
        , Svg.Attributes.style "background: #efefef"
        ]
        [ viewBall model
        ]


viewBall : Ball -> Svg.Svg Msg
viewBall { x, y } =
    circle
        [ cx <| String.fromInt x
        , cy <| String.fromInt y
        , r "10"
        ]
        []
```

We can now subscribe to the event:

```elm
module Main exposing (main)

import Browser
import Browser.Events
import Svg exposing (..)
import Svg.Attributes exposing (..)


type alias Model =
    Ball


type alias Ball =
    { x : Int
    , y : Int
    }


init : () -> ( Model, Cmd Msg )
init _ =
    ( { x = 250
      , y = 250
      }
    , Cmd.none
    )


type Msg
    = OnAnimationFrame Float


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , view = view
        , update = \_ model -> ( model, Cmd.none )
        , subscriptions = subscriptions
        }


view : Model -> Svg.Svg Msg
view model =
    svg
        [ width "500"
        , height "500"
        , viewBox "0 0 500 500"
        , Svg.Attributes.style "background: #efefef"
        ]
        [ viewBall model
        ]


viewBall : Ball -> Svg.Svg Msg
viewBall { x, y } =
    circle
        [ cx <| String.fromInt x
        , cy <| String.fromInt y
        , r "10"
        ]
        []


subscriptions : Model -> Sub Msg
subscriptions _ =
    Browser.Events.onAnimationFrameDelta OnAnimationFrame
```

If you compiled your elm files with the `--debug` option for [elm
make](https://guide.elm-lang.org/install.html#elm-make), you should see many
many messages being received in the time traveller debug window:

![OnAnimationFrame messages being listed in the time travel debugger]({static}/images/elm-pong_debug_events.png)

Let's finally add a (mostly empty) `update` function, and add a `Flags` type
alias on the unit type to clean things up a bit:

```elm
module Main exposing (main)

import Browser
import Browser.Events
import Svg exposing (..)
import Svg.Attributes exposing (..)


type alias Model =
    Ball


type alias Ball =
    { x : Int
    , y : Int
    }


init : Flags -> ( Model, Cmd Msg )
init _ =
    ( { x = 250
      , y = 250
      }
    , Cmd.none
    )


type Msg
    = OnAnimationFrame Float


type alias Flags =
    ()


main : Program Flags Model Msg
main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    ( model, Cmd.none )


view : Model -> Svg.Svg Msg
view model =
    svg
        [ width "500"
        , height "500"
        , viewBox "0 0 500 500"
        , Svg.Attributes.style "background: #efefef"
        ]
        [ viewBall model
        ]


viewBall : Ball -> Svg.Svg Msg
viewBall { x, y } =
    circle
        [ cx <| String.fromInt x
        , cy <| String.fromInt y
        , r "10"
        ]
        []


subscriptions : Model -> Sub Msg
subscriptions _ =
    Browser.Events.onAnimationFrameDelta OnAnimationFrame
```

We can be proud of ourselves: we changed a lot of code, but nothing changed
visually: the ball still isn't moving! Promise, we're moving this ball next ;)
