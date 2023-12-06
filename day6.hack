use namespace HH\Lib\IO;
use namespace HH\Lib\Str;
use namespace HH\Lib\Vec;
use namespace HH\Lib\Dict;
use namespace HH\Lib\Keyset;
use namespace HH\Lib\C;
use namespace HH\Lib\Math;

<<__EntryPoint>>
async function main(): Awaitable<void> {
    $times = vec[61, 70, 90, 66];
    $distances = vec[643, 1184, 1362, 1041];
    $output = 1;
    for ($i = 0; $i < C\count($times); ++$i) {
      $time = $times[$i];
      $distance = $distances[$i];
      $num_ways = 0;
      for ($j = 0; $j <= $time; ++$j) {
        if ($j * ($time - $j) > $distance) {
          $num_ways++;
        }
      }
      $output *= $num_ways;
    }
    echo "$output\n";
    return 0;
}
