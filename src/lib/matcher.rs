use std::collections::HashMap;
use uuid::Uuid;

#[derive(Debug)]
struct Matrix {
    size: usize,
    data: Vec<Vec<f32>>,
    uuid_index_map: HashMap<usize, Uuid>, 
}

impl Matrix {
    // Constructor to create a new matrix initialized with zeros
    fn new(size: usize) -> Self {
        Matrix {
            size,
            data: vec![vec![0.0; size]; size],
            uuid_index_map: HashMap::new(),
        }
    }

    // Method to insert a matching level into the matrix
    fn insert(&mut self, row: usize, col: usize, level: f32, uuid: Uuid) {
        if row < self.size && col < self.size {
            self.data[row][col] = level;
            let index = row * self.size + col;
            self.uuid_index_map.insert(index, uuid);
        } else {
            panic!("Invalid row or column index");
        }
    }

    // Method to retrieve a matching level from the matrix
    fn get(&self, row: usize, col: usize) -> Option<&f32> {
        if row < self.size && col < self.size {
            Some(&self.data[row][col])
        } else {
            None
        }
    }

    // Method to retrieve the UUID associated with a matrix index
    fn get_uuid(&self, row: usize, col: usize) -> Option<&Uuid> {
        let index = row * self.size + col;
        self.uuid_index_map.get(&index)
    }
}

pub struct MatcherStruct {

}