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
