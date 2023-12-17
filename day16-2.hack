use namespace HH\Lib\IO;
use namespace HH\Lib\Str;
use namespace HH\Lib\Vec;
use namespace HH\Lib\Dict;
use namespace HH\Lib\Keyset;
use namespace HH\Lib\C;
use namespace HH\Lib\Math;

enum Direccion: string as string {
  UP = "up";
  DOWN = "down";
  LEFT = "left";
  RIGHT = "right";
}
type Beam = shape(
  "direction" => Direccion,
  "loc" => (int, int),
);

function getNext((int, int) $loc, Direccion $dir): Beam {
  switch ($dir) {
    case Direccion::UP:
      $newloc = tuple($loc[0] - 1, $loc[1]);
      break;
    case Direccion::DOWN:
      $newloc = tuple($loc[0] + 1, $loc[1]);
      break;
    case Direccion::LEFT:
      $newloc = tuple($loc[0], $loc[1] - 1);
      break;
    case Direccion::RIGHT:
      $newloc = tuple($loc[0], $loc[1] + 1);
  }
  return shape("direction" => $dir, "loc" => $newloc);
}

function hashBeam(Beam $beam): string {
  return Str\format(
    "%d %d %s",
    $beam["loc"][0],
    $beam["loc"][1],
    $beam["direction"],
  );
}

function getNum(Beam $init, vec<string> $grid): int {
  $beams = vec[$init];
  $energized = keyset[];
  $seen = keyset[];

  while (true) {
    $new_energized = Keyset\map(
      $beams,
      $beam ==> Str\format("%d %d", $beam["loc"][0], $beam["loc"][1]),
    )
      |> Keyset\union($$, $energized);
    if ($energized === $new_energized) {
      return C\count($energized);
    } else {
      $energized = $new_energized;
    }
    $seen = Keyset\union($seen, Keyset\map($beams, $b ==> hashBeam($b)));
    $beams = Vec\map($beams, $beam ==> {
      $newbeams = vec[];
      $symbol = $grid[$beam["loc"][0]][$beam["loc"][1]];
      if ($symbol === ".") {
        $newbeams[] = getNext($beam["loc"], $beam["direction"]);
      } else if ($symbol === "/") {
        $curdir = $beam["direction"];
        $newdir = $curdir === Direccion::RIGHT
          ? Direccion::UP
          : (
              $curdir === Direccion::UP
                ? Direccion::RIGHT
                : (
                    $curdir === Direccion::LEFT
                      ? Direccion::DOWN
                      : Direccion::LEFT
                  )
            );
        $newbeams[] = getNext($beam["loc"], $newdir);
      } else if ($symbol === "\\") {
        $curdir = $beam["direction"];
        $newdir = $curdir === Direccion::RIGHT
          ? Direccion::DOWN
          : (
              $curdir === Direccion::UP
                ? Direccion::LEFT
                : (
                    $curdir === Direccion::LEFT
                      ? Direccion::UP
                      : Direccion::RIGHT
                  )
            );
        $newbeams[] = getNext($beam["loc"], $newdir);
      } else if ($symbol === "|") {
        if (
          $beam["direction"] === Direccion::UP ||
          $beam["direction"] === Direccion::DOWN
        ) {
          $newbeams[] = getNext($beam["loc"], $beam["direction"]);
        } else {
          $newbeams[] = getNext($beam["loc"], Direccion::UP);
          $newbeams[] = getNext($beam["loc"], Direccion::DOWN);
        }
      } else if ($symbol === "-") {
        if (
          $beam["direction"] === Direccion::LEFT ||
          $beam["direction"] === Direccion::RIGHT
        ) {
          $newbeams[] = getNext($beam["loc"], $beam["direction"]);
        } else {
          $newbeams[] = getNext($beam["loc"], Direccion::RIGHT);
          $newbeams[] = getNext($beam["loc"], Direccion::LEFT);
        }
      }
      $newbeams = Vec\filter(
        $newbeams,
        $beam ==> $beam["loc"][0] >= 0 &&
          $beam["loc"][1] >= 0 &&
          $beam["loc"][0] < C\count($grid) &&
          $beam["loc"][1] < Str\length($grid[0]) &&
          !C\contains($seen, hashBeam($beam)),
      );
      return $newbeams;
    }) |> Vec\flatten($$);
  }
}

<<__EntryPoint>>
async function main(): Awaitable<void> {
  $in = await IO\request_input()->readAllAsync();
  $grid = Str\split($in, "\n") |> Vec\filter($$, $s ==> $s !== "");
  $max = 0;
  for ($i = 0; $i < C\count($grid); ++$i) {
    $max = Math\maxva($max, getNum(
      shape("direction" => Direccion::RIGHT, "loc" => tuple($i, 0)),
      $grid,
    ));
    $max = Math\maxva($max, getNum(
      shape(
        "direction" => Direccion::LEFT,
        "loc" => tuple($i, Str\length($grid[0]) - 1),
      ),
      $grid,
    ));
  }
  for ($j = 0; $j < Str\length($grid[0]); ++$j) {
    $max = Math\maxva($max, getNum(
      shape("direction" => Direccion::DOWN, "loc" => tuple(0, $j)),
      $grid,
    ));
    $max = Math\maxva($max, getNum(
      shape(
        "direction" => Direccion::UP,
        "loc" => tuple(C\count($grid) - 1, $j),
      ),
      $grid,
    ));
  }
  echo $max."\n";
}
