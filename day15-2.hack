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

type lens = shape(
  'label' => string,
  'power' => int,
);

<<__EntryPoint>>
async function main(): Awaitable<void> {
  $boxes = Dict\fill_keys(Vec\range(0, 256), vec[]);

  $lines = await IO\request_input()->readAllAsync()
    |> Str\replace($$, "\n", "")
    |> Str\split($$, ",");
  foreach ($lines as $line) {

    if (Str\ends_with($line, "-")) {
      $label = Str\split($line, '-')[0];
      $hash = run_hash_algo($label);
      $boxes[$hash] =
        Vec\filter($boxes[$hash], (lens $lens) ==> $lens['label'] !== $label);
    } else {
      $label = Str\split($line, "=")[0];
      $hash = run_hash_algo($label);
      $focallength = Str\split($line, "=")[1] |> (int)$$;
      $boxes[$hash] = Vec\map($boxes[$hash], (lens $lens) ==> {
        if ($lens['label'] !== $label) {
          return $lens;
        }
        return shape('label' => $label, 'power' => $focallength);
      });
      if (!C\any($boxes[$hash], $lens ==> $lens['label'] === $label)) {
        $boxes[$hash][] = shape('label' => $label, 'power' => $focallength);
      }

    }
  }
  $output = 0;
  for ($i = 0; $i < 256; ++$i) {
    for ($j = 0; $j < C\count($boxes[$i]); ++$j) {
      $output += ($i + 1) * ($j + 1) * $boxes[$i][$j]['power'];
    }
  }
  echo $output;
}
