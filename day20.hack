use namespace HH\Lib\IO;
use namespace HH\Lib\Str;
use namespace HH\Lib\Vec;
use namespace HH\Lib\Dict;
use namespace HH\Lib\Keyset;
use namespace HH\Lib\C;
use namespace HH\Lib\Math;

enum modtype: string {
  BROADCASTER = "broadcaster";
  FLIPFLOP = "flipflop";
  CONJUNCTION = "conjunction";
}

enum onoff: string {
  ON = "on";
  OFF = "off";
}

enum lowhigh: string {
  LOW = "low";
  HIGH = "high";
}

type mod = shape(
  'type' => modtype,
  'dests' => vec<string>,
  ?'flipflopstate' => onoff,
  'conjunctionstate' => dict<string, lowhigh>,
);

function push_button(inout dict<string, mod> $modules): (int, int) {
  $q = vec[tuple("broadcaster", lowhigh::LOW, "button")];
  $low = 0;
  $high = 0;
  while (!C\is_empty($q)) {
    list($name, $pulse, $prev) = C\pop_frontx(inout $q);
    if ($name === "rx" && $pulse === lowhigh::LOW) {
      throw new Exception("Push button $name");
    }
    // echo "$prev -$pulse-> $name\n";
    if ($pulse === lowhigh::LOW) {
      $low++;
    } else {
      $high++;
    }
    $node = $modules[$name] ?? null;
    if ($node is null) {
      continue;
    }
    switch ($node['type']) {
      case modtype::BROADCASTER:
        foreach ($node['dests'] as $dest) {
          $q[] = tuple($dest, lowhigh::LOW, $name);
        }
        break;
      case modtype::FLIPFLOP:
        if ($pulse === lowhigh::LOW) {
          $modules[$name]['flipflopstate'] =
            Shapes::idx($node, 'flipflopstate') === onoff::ON
              ? onoff::OFF
              : onoff::ON;
          foreach ($node['dests'] as $dest) {
            $q[] = tuple(
              $dest,
              Shapes::idx($node, 'flipflopstate') === onoff::ON
                ? lowhigh::LOW
                : lowhigh::HIGH,
              $name,
            );
          }
        }
        break;
      case modtype::CONJUNCTION:
        $modules[$name]['conjunctionstate'][$prev] = $pulse;
        $pulsetosend = (
          C\every(
            $modules[$name]['conjunctionstate'],
            $x ==> $x === lowhigh::HIGH,
          )
        )
          ? lowhigh::LOW
          : lowhigh::HIGH;
        foreach ($node['dests'] as $dest) {
          $q[] = tuple($dest, $pulsetosend, $name);
        }
    }
  }
  return tuple($low, $high);
}

<<__EntryPoint>>
async function main(): Awaitable<void> {
  $in = await IO\request_input()->readAllAsync();
  $lines = Str\split($in, "\n");
  $modules = dict[];
  foreach ($lines as $line) {
    if ($line === "") {
      continue;
    }
    $line = Str\split($line, ' -> ');
    $name = $line[0];
    $type = modtype::BROADCASTER;
    if ($name !== "broadcaster") {
      $t = Str\slice($name, 0, 1);
      $type = $t === '%' ? modtype::FLIPFLOP : modtype::CONJUNCTION;
      $name = Str\slice($name, 1);
    }
    $dests = Str\split($line[1], ', ');
    $module = shape('type' => $type, 'dests' => $dests);
    if ($type === modtype::FLIPFLOP) {
      $module['flipflopstate'] = onoff::OFF;
    } else if ($type === modtype::CONJUNCTION) {
    }
    $module['conjunctionstate'] = dict[];
    $modules[$name] = $module;
  }

  foreach ($modules as $name => $module) {
    foreach ($module['dests'] as $dest) {
      if (($modules[$dest]['type'] ?? null) === modtype::CONJUNCTION) {
        $state = $modules[$dest]['conjunctionstate'] ?? dict[];
        $state[$name] = lowhigh::LOW;
        $modules[$dest]['conjunctionstate'] = $state;
      }
    }
  }

  list($low, $high) = tuple(0, 0);
  for ($i = 0; $i < 1000000000; $i++) {
    echo("\nIteration $i");
    list($l, $h) = push_button(inout $modules);
    $low += $l;
    $high += $h;
  }
  $output = $low * $high;
  echo("$low, $high, $output\n");
}
