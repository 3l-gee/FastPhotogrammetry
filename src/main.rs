mod lib {
    pub mod image;
}

use std::time::Instant;
use lib::image::{ImageStruct, ImageProcessing};

fn main() {
    let start = Instant::now();

    
    let image_path = "C:/Users/Raphael_Gerth/Documents/HOME/FUNTIMES_Rust/photogrametry/img/PXL_20240317_082231220.jpg"; // Replace with the actual path to your image file
    
    //Load
    let load_start = start.elapsed();

    let mut image = match crate::ImageStruct::load(image_path) {
        Ok(image) => image,
        Err(err) => {
            eprintln!("Error loading image: {}", err);
            return;
        }
    };

    image.info();

    let load_end = start.elapsed();
    println!("Load {:?}", load_end - load_start);

    //Process
    let process_start = start.elapsed();

    image.process();

    let process_end = start.elapsed();
    println!("Process {:?}", process_end - process_start);
    

    //Save
    let save_start = start.elapsed();

    match image.save() {
        Ok(()) => println!("Image saved successfully."),
        Err(err) => eprintln!("Error saving image: {}", err),
    }
    
    let save_end = start.elapsed();
    println!("Save {:?}", save_end - save_start);

    println!("All {:?}", start.elapsed());
}