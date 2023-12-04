use namespace HH\Lib\IO;
use namespace HH\Lib\Str;
use namespace HH\Lib\Vec;
use namespace HH\Lib\Math;

<<__EntryPoint>>
async function main(): Awaitable<void> {
  $in = await IO\request_input()->readAllAsync();
  $lines = Str\split($in, "\n");
  $output = 0;
  foreach ($lines as $line) {
    if ($line === "") {
      continue;
    }
    $game_number =
        Str\split($line, ": ")[0] |> Str\split($$, " ")[1] |> (int)$$;
    $draws = Str\split($line, ": ")[1]
      |> Str\split($$, "; ")
      |> Vec\map($$, $g ==> {
        list($red, $green, $blue) = tuple(0, 0, 0);
        $colors = Str\split($g, ", ");
        foreach ($colors as $color) {
          if (Str\contains($color, "red")) {
            $red = Str\split($color, " ")[0] |> (int)$$;
          } else if (Str\contains($color, "green")) {
            $green = Str\split($color, " ")[0] |> (int)$$;
          } else if (Str\contains($color, "blue")) {
            $blue = Str\split($color, " ")[0] |> (int)$$;
          }
        }
        return tuple($red, $green, $blue);
      });
    list($red, $green, $blue) = tuple(0, 0, 0);
    foreach ($draws as $draw) {
      $red = Math\max(vec[$red, $draw[0]]) as nonnull;
      $green = Math\max(vec[$green, $draw[1]]) as nonnull;
      $blue = Math\max(vec[$blue, $draw[2]]) as nonnull;
    }
    $power = $red * $blue * $green;
    $output += $power;
  }
  $output = (string)$output;
  await IO\request_output()->writeAllAsync($output."\n");
}
