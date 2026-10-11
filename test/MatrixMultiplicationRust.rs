fn matrix_multiply(a: &Vec<i32>, b: &Vec<i32>, size: usize) -> Vec<i32> {
    let mut result = vec![0; size * size];

    for i in 0..size {
        for k in 0..size {
            let val_a = a[i * size + k];
            for j in 0..size {
                result[i * size + j] += val_a * b[k * size + j];
            }
        }
    }

    result
}

fn main() {
    let size = 500;

    let a = vec![1; size * size];
    let b = vec![1; size * size];

    let _result = matrix_multiply(&a, &b, size);

    println!("Done");
}