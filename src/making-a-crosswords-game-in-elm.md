Title: Making a crosswords game in elm
Date: 2020-03-14 19:21
Category: elm
Tags: gamedev


After having made a graphical and animated [game of pong]({filename}/making-a-pong-game-in-elm.md) in
[elm](https://elm-lang.org/), let's now make a crosswords game by taking [tiny
steps](https://medium.com/@dillonkearns/moving-faster-with-tiny-steps-in-elm-2e6a269e4efc).

The game of pong helped us understand how to draw using SVG, and how to
subscribe to time events. In this series of blog posts, we're going to delve
into the dom manipulation, dom events and so on. I'm already excited, are you?

If you haven't already, the very first step is to [install
elm](https://guide.elm-lang.org/install.html), and to keep in mind that the
folks on [the slack channel](https://elmlang.herokuapp.com/) are very friendly and
helpful if you ever face an issue that you can't manage to solve on your own.
You are not alone!


## Create the project

We've seen this already in the first chapters of the [game of pong]({filename}/making-a-pong-game-in-elm.md) blog post, so we're not explaining it again here. Also instead of using the trusted `elm make` we're going straight for `elm-live` and its live reloading capabilities!

Running `elm-live src/Main.elm` will compile successfully and start a web
server for us on http://localhost:8000.

The `Main.elm` file is the same basic one as for the game of pong:

```elm
module Main exposing (main)

import Html


main =
    Html.text "Hello world!"
```

[Source code up to this point](https://github.com/magopian/elm-crosswords/tree/0-create-project).


## Display a grid of cells

A crossword puzzle is represented as a grid of cells, either white (will need a letter) or black (a word separator or filler). For now, as our first baby step, let's display a grid of 9 cells, arranged in three lines and thee columns:

```elm
module Main exposing (main)

import Html
import Html.Attributes


main =
    Html.div
        [ Html.Attributes.style "background-color" "#000"
        , Html.Attributes.style "height" "500px"
        , Html.Attributes.style "width" "500px"
        , Html.Attributes.style "display" "grid"
        , Html.Attributes.style "grid-template-columns" "repeat(3, 1fr)"
        , Html.Attributes.style "grid-auto-rows" "1fr"
        , Html.Attributes.style "grid-gap" "1px"
        , Html.Attributes.style "padding" "1px"
        ]
        [ Html.div [ Html.Attributes.style "background-color" "#fff" ] []
        , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
        , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
        , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
        , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
        , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
        , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
        , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
        , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
        ]

```

This does display a pretty neat "all white cells" grid.

![the 3x3 grid]({static}/images/elm-crosswords/3x3_grid.png)

We're using a [grid
layout](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Grids)
as it's perfectly adapted to our use case. We could also have used a table,
but the markup is way longer, and the end result is harder to style.

This code is however very unmaintainable. What if we wanted to display a 4x4
grid, or a 12x12? We would need to go through the style declaration, and
manually copy/paste all the individual cells. Let's change this a bit by
having a width that we can store in a top-level variable for now:

```diff
 import Html.Attributes
 
 
+gridWidth =
+    3
+
+
 main =
     Html.div
         [ Html.Attributes.style "background-color" "#000"
         , Html.Attributes.style "height" "500px"
         , Html.Attributes.style "width" "500px"
         , Html.Attributes.style "display" "grid"
-        , Html.Attributes.style "grid-template-columns" "repeat(3, 1fr)"
+        , Html.Attributes.style
+            "grid-template-columns"
+            ("repeat(" ++ String.fromInt gridWidth ++ ", 1fr)")
         , Html.Attributes.style "grid-auto-rows" "1fr"
         , Html.Attributes.style "grid-gap" "1px"
         , Html.Attributes.style "padding" "1px"
```

Let's extract that "grid-template-columns" calculation in a function:

```diff
@@ -14,9 +14,7 @@ main =
         , Html.Attributes.style "height" "500px"
         , Html.Attributes.style "width" "500px"
         , Html.Attributes.style "display" "grid"
-        , Html.Attributes.style
-            "grid-template-columns"
-            ("repeat(" ++ String.fromInt gridWidth ++ ", 1fr)")
+        , Html.Attributes.style "grid-template-columns" <| gridTemplateColumns gridWidth
         , Html.Attributes.style "grid-auto-rows" "1fr"
         , Html.Attributes.style "grid-gap" "1px"
         , Html.Attributes.style "padding" "1px"
@@ -31,3 +29,8 @@ main =
         , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
         , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
         ]
+
+
+gridTemplateColumns : Int -> String
+gridTemplateColumns width =
+    "repeat(" ++ String.fromInt width ++ ", 1fr)"
```

This is way more readable. How about going one step further and changing the `gridTemplateColumns` function to return an `Html.Attribute` type that we could use as is?

```diff
@@ -14,7 +14,7 @@ main =
         , Html.Attributes.style "height" "500px"
         , Html.Attributes.style "width" "500px"
         , Html.Attributes.style "display" "grid"
-        , Html.Attributes.style "grid-template-columns" <| gridTemplateColumns gridWidth
+        , gridTemplateColumns gridWidth
         , Html.Attributes.style "grid-auto-rows" "1fr"
         , Html.Attributes.style "grid-gap" "1px"
         , Html.Attributes.style "padding" "1px"
@@ -31,6 +31,8 @@ main =
         ]
 
 
-gridTemplateColumns : Int -> String
+gridTemplateColumns : Int -> Html.Attribute ()
 gridTemplateColumns width =
-    "repeat(" ++ String.fromInt width ++ ", 1fr)"
+    Html.Attributes.style
+        "grid-template-columns"
+        ("repeat(" ++ String.fromInt width ++ ", 1fr)")
```

In our search of readability, it would make sense to factor out the grid styles into its own function too:

```diff
@@ -10,15 +10,7 @@ gridWidth =
 
 main =
     Html.div
-        [ Html.Attributes.style "background-color" "#000"
-        , Html.Attributes.style "height" "500px"
-        , Html.Attributes.style "width" "500px"
-        , Html.Attributes.style "display" "grid"
-        , gridTemplateColumns gridWidth
-        , Html.Attributes.style "grid-auto-rows" "1fr"
-        , Html.Attributes.style "grid-gap" "1px"
-        , Html.Attributes.style "padding" "1px"
-        ]
+        (gridStyle gridWidth)
         [ Html.div [ Html.Attributes.style "background-color" "#fff" ] []
         , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
         , Html.div [ Html.Attributes.style "background-color" "#fff" ] []
@@ -31,6 +23,19 @@ main =
         ]
 
 
+gridStyle : Int -> List (Html.Attribute ())
+gridStyle width =
+    [ Html.Attributes.style "background-color" "#000"
+    , Html.Attributes.style "height" "500px"
+    , Html.Attributes.style "width" "500px"
+    , Html.Attributes.style "display" "grid"
+    , gridTemplateColumns width
+    , Html.Attributes.style "grid-auto-rows" "1fr"
+    , Html.Attributes.style "grid-gap" "1px"
+    , Html.Attributes.style "padding" "1px"
+    ]
+
+
 gridTemplateColumns : Int -> Html.Attribute ()
 gridTemplateColumns width =
     Html.Attributes.style
```

If you're wondering what are those `()`, we've adressed that in the pong
game: it's the [unit
type](https://package.elm-lang.org/packages/elm/core/latest/Basics#Never).
Don't worry too much about it, we'll soon replace those with a `Msg` type.

Ok so now we have a grid that's displayed given its width. But wait, what happens if we change the width to 4?

![the 4x3 grid]({static}/images/elm-crosswords/4x3_grid.png)

That's because the grid is indeed 4 columns wide, and still 3 lignes height,
because we defined 9 cells (4*3 = 12 cells). That's pretty and all, but
useless. We don't want to have to add those missing cells manually. Instead
we want the grid to also have a height.

So the idea is to loop on the height (the rows), and for each row loop on the
width (the cells).

But wait, there is no `for` instruction in elm. Instead, there's `List.map`
for example, which will "loop" on each of the list items. And we can create a
list of an arbitrary length using `List.range`, which takes a starting and
ending index.

```elm
List.range 1 4
```

Will produce a list of 4 integers `[1, 2, 3, 4]`. We can then `List.map` on
it and output a cell for each integer. Be careful, in elm `List.range` is
different than in python for example where the ending index is NOT included.
In elm, the ending index IS included. This is why, to have a list of length 4
we start at 1 instead of the usual 0.

```elm
gridRow : Int -> List (Html.Html ())
gridRow width =
    List.range 1 width
        |> List.map (\_ -> gridCell)


gridCell : Html.Html ()
gridCell =
    Html.div [ Html.Attributes.style "background-color" "#fff" ] []
```

Calling `gridRow 4` will output a row of four cells:

```elm
[ Html.div [ Html.Attributes.style "background-color" "#fff" ] []
, Html.div [ Html.Attributes.style "background-color" "#fff" ] []
, Html.div [ Html.Attributes.style "background-color" "#fff" ] []
, Html.div [ Html.Attributes.style "background-color" "#fff" ] []
]
```

We can repeat this process `gridHeight` times using a `List.range` once again:

```elm
grid : Int -> Int -> List (List (Html.Html ()))
grid width height =
    List.range 1 height
        |> List.map (\_ -> gridRow width)
```

Careful once again: this will return a list of a list rows:

```elm
[ [<cell1>, <cell2>, <cell3>, <cell4>]
, [<cell1>, <cell2>, <cell3>, <cell4>]
, [<cell1>, <cell2>, <cell3>, <cell4>]
]
```

But the grid div will want a list, not a list of list, so we have to
`List.concat` it. The final result is there:

```elm
module Main exposing (main)

import Html
import Html.Attributes


gridWidth =
    4


gridHeight =
    3


main =
    Html.div
        (gridStyle gridWidth)
        (List.concat <| grid gridWidth gridHeight)


gridStyle : Int -> List (Html.Attribute ())
gridStyle width =
    [ Html.Attributes.style "background-color" "#000"
    , Html.Attributes.style "height" "500px"
    , Html.Attributes.style "width" "500px"
    , Html.Attributes.style "display" "grid"
    , gridTemplateColumns width
    , Html.Attributes.style "grid-auto-rows" "1fr"
    , Html.Attributes.style "grid-gap" "1px"
    , Html.Attributes.style "padding" "1px"
    ]


gridTemplateColumns : Int -> Html.Attribute ()
gridTemplateColumns width =
    Html.Attributes.style
        "grid-template-columns"
        ("repeat(" ++ String.fromInt width ++ ", 1fr)")


grid : Int -> Int -> List (List (Html.Html ()))
grid width height =
    List.range 1 height
        |> List.map (\_ -> gridRow width)


gridRow : Int -> List (Html.Html ())
gridRow width =
    List.range 1 width
        |> List.map (\_ -> gridCell)


gridCell : Html.Html ()
gridCell =
    Html.div [ Html.Attributes.style "background-color" "#fff" ] []

```

[Source code up to this point](https://github.com/magopian/elm-crosswords/tree/1-display-4x3-grid).
