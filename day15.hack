use namespace HH\Lib\IO;
use namespace HH\Lib\Str;
use namespace HH\Lib\Vec;
use namespace HH\Lib\Dict;
use namespace HH\Lib\Keyset;
use namespace HH\Lib\C;
use namespace HH\Lib\Math;

function run_hash_algo(string $str): int {
  $hash = 0;
  for ($i = 0; $i < Str\length($str); ++$i) {
    $a = ord($str[$i]);
    $hash += $a;
    $hash *= 17;
    $hash %= 256;
  }
  return $hash;
}

<<__EntryPoint>>
async function main(): Awaitable<void> {
  await IO\request_input()->readAllAsync()
    |> Str\replace($$, "\n", "")
    |> Str\split($$, ",")
    |> Vec\map($$, $line ==> run_hash_algo($line))
    |> Math\sum($$)
    |> print($$."\n");
}
