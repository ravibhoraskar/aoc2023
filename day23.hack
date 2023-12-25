use namespace HH\Lib\IO;
use namespace HH\Lib\Str;
use namespace HH\Lib\Vec;
use namespace HH\Lib\Dict;
use namespace HH\Lib\Keyset;
use namespace HH\Lib\C;
use namespace HH\Lib\Math;

<<__EntryPoint>>
async function main(): Awaitable<void> {
  $in = await IO\request_input()->readAllAsync();
  $grid = Str\split($in, "\n") |> Vec\filter($$, $s ==> $s !== "");
  $end = C\count($grid) - 1;

  $queue = vec[shape(
    'toprocess' => tuple(0, 1),
    'pathsofar' => vec[],
  )];
  $pathlengths = vec[];
  while (!C\is_empty($queue)) {
    $entry = C\pop_frontx(inout $queue);

    list($i, $j) = $entry['toprocess'];
    // i < 0 or j < 0 or i >= len(m) or j >= len(m[0]):
    if (
      $i < 0 || $j < 0 || $i >= C\count($grid) || $j >= Str\length($grid[0])
    ) {
      continue;
    } else if ($grid[$i][$j] === '#') {
      continue;
    } else if (C\contains($entry['pathsofar'], tuple($i, $j))) {
      continue;
    } else if ($i === $end) {
      $pathlength = C\count($entry['pathsofar']);
      $pathlengths[] = $pathlength;
    } else if ($grid[$i][$j] === '>') {
      $queue[] = shape(
        'toprocess' => tuple($i, $j + 1),
        'pathsofar' => Vec\concat($entry['pathsofar'], vec[tuple($i, $j)]),
      );
    } else if ($grid[$i][$j] === 'v') {
      $queue[] = shape(
        'toprocess' => tuple($i + 1, $j),
        'pathsofar' => Vec\concat($entry['pathsofar'], vec[tuple($i, $j)]),
      );
    } else {
      $newpathsofar = Vec\concat($entry['pathsofar'], vec[tuple($i, $j)]);
      $queue[] = shape(
        'toprocess' => tuple($i + 1, $j),
        'pathsofar' => $newpathsofar,
      );
      $queue[] = shape(
        'toprocess' => tuple($i, $j + 1),
        'pathsofar' => $newpathsofar,
      );
      $queue[] = shape(
        'toprocess' => tuple($i - 1, $j),
        'pathsofar' => $newpathsofar,
      );
      $queue[] = shape(
        'toprocess' => tuple($i, $j - 1),
        'pathsofar' => $newpathsofar,
      );
    }
  }
  $answer = Math\max($pathlengths) as nonnull;
  echo("Answer is $answer");
  return 0;
}
