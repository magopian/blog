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

