use namespace HH\Lib\IO;
use namespace HH\Lib\Str;
use namespace HH\Lib\Vec;
use namespace HH\Lib\Dict;
use namespace HH\Lib\Keyset;
use namespace HH\Lib\C;
use namespace HH\Lib\Math;
use namespace HH\Lib\PseudoRandom;

<<__Memoize>>
function get_neighbors(vec<string> $grid, int $i, int $j): vec<(int, int)> {
  return vec[
    tuple($i + 1, $j),
    tuple($i - 1, $j),
    tuple($i, $j + 1),
    tuple($i, $j - 1),
  ]
    |> Vec\filter(
      $$,
      $t ==> $t[0] >= 0 &&
        $t[1] >= 0 &&
        $t[0] < C\count($grid) &&
        $t[1] < Str\length($grid[0]),
    )
    |> Vec\filter($$, $nbr ==> $grid[$nbr[0]][$nbr[1]] !== '#');
}

<<__Memoize>>
function getNextDecisionPoint(
  vec<string> $grid,
  int $i,
  int $j,
  vec<(int, int)> $decision_points,
): ((int, int), keyset<string>) {
  $prev = tuple($i, $j);
  $seen = keyset[hashcoord($prev)];
  $cur = get_neighbors($grid, $i, $j)
    |> Vec\filter($$, $c ==> !C\contains($decision_points, $c))
    |> C\onlyx($$);
  while (!C\contains($decision_points, $cur)) {
    $seen[] = hashcoord($cur);
    $next = get_neighbors($grid, $cur[0], $cur[1])
      |> Vec\filter($$, $c ==> $c !== $prev)
      |> C\onlyx($$);
    $prev = $cur;
    $cur = $next;
  }
  $seen[] = hashcoord($cur);
  return tuple($cur, $seen);
}

<<__Memoize>>
function hashcoord((int, int) $p): string {
  return Str\format("%d,%d", $p[0], $p[1]);
}

<<__Memoize>>
function unhashcoord(string $h): (int, int) {
  list($i, $j) = Str\split($h, ",");
  return tuple((int)$i, (int)$j);
}

function append(
  inout dict<string, vec<shape('nbr' => string, 'distance' => int)>> $graph,
  string $from,
  shape('nbr' => string, 'distance' => int) $edge,
): void {
  if (!C\contains_key($graph, $from)) {
    $graph[$from] = vec[];
  }
  $graph[$from][] = $edge;
}

<<__EntryPoint>>
async function main(): Awaitable<void> {
  $in = await IO\request_input()->readAllAsync();
  $grid = Str\split($in, "\n") |> Vec\filter($$, $s ==> $s !== "");
  $end = C\count($grid) - 1;

  $decision_points = vec[tuple(0, 1)];
  for ($i = 0; $i < C\count($grid); $i++) {
    for ($j = 0; $j < Str\length($grid[0]); $j++) {
      if ($grid[$i][$j] === '#') {
        $nbr_count = 0;
      } else {
        $nbr_count = get_neighbors($grid, $i, $j)
          |> Vec\map($$, $nbr ==> $grid[$nbr[0]][$nbr[1]])
          |> C\count($$);
      }
      if ($nbr_count > 2) {
        $decision_points[] = tuple($i, $j);
      }
    }
  }
  $end_node = null;
  for ($j = 0; $j < Str\length($grid[0]); $j++) {
    if ($grid[C\count($grid) - 1][$j] !== '#') {
      $node = tuple(C\count($grid) - 1, $j);
      $decision_points[] = $node;
      $end_node = hashcoord($node);
    }
  }
  $end_node = $end_node as nonnull;

  $graph = dict[];
  foreach ($decision_points as $dp) {
    $neighbors = get_neighbors($grid, $dp[0], $dp[1]);
    foreach ($neighbors as $nbr) {
      list($next_decision_point, $seen) =
        getNextDecisionPoint($grid, $nbr[0], $nbr[1], $decision_points);
      append(
        inout $graph,
        hashcoord($dp),
        shape(
          'nbr' => hashcoord($next_decision_point),
          'distance' => C\count($seen),
        ),
      );
    }
  }

  $queue = vec[shape(
    'toprocess' => "0,1",
    'pathsofar' => keyset[],
    'lengthsofar' => 0,
  )];
  $pathlengths = vec[];
  while (!C\is_empty($queue)) {
    $entry = C\pop_backx(inout $queue);
    $node = $entry['toprocess'];
    $pathlength = $entry['lengthsofar'];
    $pathsofar = $entry['pathsofar'];
    if (C\contains($entry['pathsofar'], $node)) {
      // Found a cycle, stop processing
      continue;
    } else if ($node === $end_node) {
      $pathlengths[] = $pathlength;
      if (PseudoRandom\int(0, 10000) < 10) {
        $max = Math\max($pathlengths) as nonnull;
        echo("Found a path of length $pathlength, max so far is $max \n");
      }
    } else {
      $newpathsofar = Keyset\union($pathsofar, keyset[$node]);
      foreach ($graph[$node] as $next) {
        $queue[] = shape(
          'toprocess' => $next['nbr'],
          'pathsofar' => $newpathsofar,
          'lengthsofar' => $pathlength + $next['distance'],
        );
      }
    }
  }
  $answer = Math\max($pathlengths) as nonnull;
  echo("Answer is $answer\n");
}
