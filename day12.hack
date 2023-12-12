use namespace HH\Lib\IO;
use namespace HH\Lib\Str;
use namespace HH\Lib\Vec;
use namespace HH\Lib\Dict;
use namespace HH\Lib\Keyset;
use namespace HH\Lib\C;
use namespace HH\Lib\Math;

<<__Memoize>>
function get_count(
  vec<string> $springs,
  vec<int> $combos,
  bool $group_started,
): int {
  if (C\is_empty($springs)) {
    return C\is_empty($combos) || ($combos[0] === 0 && C\count($combos) === 1)
      ? 1
      : 0;
  } else if ($springs[0] === '.') {
    if ($group_started) {
      if ($combos[0] === 0) {
        return get_count(Vec\drop($springs, 1), Vec\drop($combos, 1), false);
      } else {
        return 0;
      }
    } else {
      return get_count(Vec\drop($springs, 1), $combos, false);
    }
  } else if ($springs[0] === '#') {
    if (C\is_empty($combos) || $combos[0] === 0) {
      return 0;
    } else {
      return get_count(
        Vec\drop($springs, 1),
        Vec\concat(vec[$combos[0] - 1], Vec\drop($combos, 1)),
        true,
      );
    }
  } else if ($springs[0] === '?') {
    return get_count(
      Vec\concat(vec['.'], Vec\drop($springs, 1)),
      $combos,
      $group_started,
    ) +
      get_count(
        Vec\concat(vec['#'], Vec\drop($springs, 1)),
        $combos,
        $group_started,
      );
  } else {
    throw new Exception("Invalid input");
  }
}

<<__EntryPoint>>
async function main(): Awaitable<void> {
  $in = await IO\request_input()->readAllAsync();
  $lines = Str\split($in, "\n");
  $output = 0;
  foreach ($lines as $line) {
    if ($line === "") {
      continue;
    }
    $springs = Str\split($line, " ")[0] |> Str\split($$, '');
    $combos = Str\split($line, " ")[1]
      |> Str\split($$, ",")
      |> Vec\map($$, $v ==> (int)$v);
    $num = get_count($springs, $combos, false);
    $output += $num;
  }
  echo "$output\n";
}
