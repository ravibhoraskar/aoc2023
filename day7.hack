use namespace HH\Lib\IO;
use namespace HH\Lib\Str;
use namespace HH\Lib\Vec;
use namespace HH\Lib\Dict;
use namespace HH\Lib\Keyset;
use namespace HH\Lib\C;
use namespace HH\Lib\Math;

const vec<string> CARDS =
  vec['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];

<<__EntryPoint>>
async function main(): Awaitable<void> {
  $in = await IO\request_input()->readAllAsync();
  $lines = Str\split($in, "\n");
  $hands = vec[];

  foreach ($lines as $line) {
    if ($line === "") {
      continue;
    }
    $splitline = Str\split($line, ' ');
    $hands[] = tuple($splitline[0], (int)$splitline[1]);
  }
  $sorted = Vec\sort_by($hands, $hand ==> {
    $card = $hand[0];
    $type = getType($hand[0]);
    $score = $type * 10000000000;
    for ($i = 0; $i < 5; ++$i) {
      $posscore = C\find_key(Vec\reverse(CARDS), $c ==> $c === $card[$i])
        as nonnull;

      $posscore = $posscore * (15 ** (6 - $i));
      $posscore = (int)$posscore;
      $score += $posscore;
    }
    return $score;
  });
  $score = 0;
  for ($i = 0; $i < C\count($sorted); ++$i) {
    $score += $sorted[$i][1] * ($i + 1);
  }
  echo "Score: $score\n";
}

function getType(string $card): int {
  $cards = Str\split($card, '') |> Dict\count_values($$);
  $counts = Vec\sort($cards) |> Vec\reverse($$);
  if ($counts[0] === 5) {
    return 7;
  } else if ($counts[0] === 4) {
    return 6;
  } else if ($counts[0] === 3) {
    if ($counts[1] === 2) {
      return 5;
    } else {
      return 4;
    }
  } else if ($counts[0] === 2) {
    if ($counts[1] === 2) {
      return 3;
    } else {
      return 2;
    }
  } else {
    return 1;
  }
}
