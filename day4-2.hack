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
  $lines = Str\split($in, "\n");
  $cards = Vec\range(1, 187) |> Dict\pull($$, $_ ==> 1, $k ==> $k);
  $i = 1;
  foreach ($lines as $line) {
    if ($line === "") {
      continue;
    }
    $split = Str\split($line, ': ')[1] |> Str\split($$, " | ");
    $winning_numbers = $split[0]
      |> Str\split($$, ' ')
      |> Keyset\filter($$, $s ==> $s !== "")
      |> Keyset\map($$, $num ==> (int)$num);
    $numbers_i_have = $split[1]
      |> Str\split($$, ' ')
      |> Keyset\filter($$, $s ==> $s !== "")
      |> Keyset\map($$, $num ==> (int)$num);
    $num_nums = C\count(Keyset\intersect($winning_numbers, $numbers_i_have));
    for ($j = 0; $j < $num_nums; $j++) {
      $cards[$i + 1 + $j] += $cards[$i];
    }
    $i++;
  }
  echo Str\format("%d\n", Math\sum($cards));
}
