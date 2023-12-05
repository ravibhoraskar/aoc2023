fn main() {
    let stdin = std::io::stdin();

    let mut seeds = String::new();
    let _ = stdin.read_line(&mut seeds);

    let (_header, rest) = seeds.split_once(':').unwrap();
    let input: Vec<u64> = rest
        .split_whitespace()
        .map(|n| n.parse().unwrap())
        .collect();
    let mut seeds = vec![];
    for i in (0..input.len()).step_by(2) {
        seeds.extend(input[i]..input[i] + input[i + 1]);
    }
    let mut emptyline = String::new();
    let _ = stdin.read_line(&mut emptyline);

    let mut map = vec![];
    let mut next_seeds = seeds.clone();

    for line in stdin.lines() {
        let line = line.unwrap();
        if line.eq("") {
            // Finished constucting map
            for seed in seeds.as_slice() {
                let mapped = map
                    .iter()
                    .find(|(_, src, range)| *seed >= *src && *seed < *src + *range);
                let next = match mapped {
                    Some((dst, src, _)) => *seed - *src + *dst,
                    None => *seed,
                };
                next_seeds.push(next);
            }
        } else if line.ends_with(':') {
            map = vec![];
            seeds = next_seeds;
            next_seeds = vec![];
        } else {
            let imp: Vec<u64> = line
                .split_whitespace()
                .map(|n| n.parse().unwrap())
                .collect();
            map.push((imp[0], imp[1], imp[2]));
        }
    }
    println!("final answer is {}", next_seeds.iter().min().unwrap());
}
