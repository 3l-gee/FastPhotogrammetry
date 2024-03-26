#[warn(non_snake_case)]
mod lib {
    pub mod image;
    pub mod imageBucket;
}

use std::path::Path;

// use std::path::Path;
use lib::imageBucket::{ImageBucketStruct,ImageBucketActions};

fn main() { 

    let path = Path::new("C:/Users/Raphael_Gerth/Documents/HOME/FUNTIMES_Rust/photogrametry/img");
    let image_name_list = vec![
        "PXL_20240317_082324792.jpg".to_string(),
        "PXL_20240317_082319750.jpg".to_string(),
        "PXL_20240317_082309262.jpg".to_string(),
        "PXL_20240317_082303565.jpg".to_string(),
        "PXL_20240317_082254819.jpg".to_string(),
        "PXL_20240317_082249759.jpg".to_string(),
        "PXL_20240317_082245096.jpg".to_string(),
        "PXL_20240317_082239261.jpg".to_string(),
    ];

    let mut tool = crate::ImageBucketStruct::new();

    tool.add_load_images(path, image_name_list);

    tool.execute(ImageBucketActions::Info);

    tool.execute(ImageBucketActions::Process);

    tool.execute(ImageBucketActions::Compute);

    tool.execute(ImageBucketActions::Draw);

    tool.execute(ImageBucketActions::Info);

    tool.execute(ImageBucketActions::Save);

}

    // let load_start = start.elapsed();

    // let mut image = match crate::ImageStruct::load(image_path) {
    //     Ok(image) => image,
    //     Err(err) => {
    //         eprintln!("Error loading image: {}", err);
    //         return;
    //     }
    // };

    // //info
    // image.info();



    // let load_end = start.elapsed();
    // println!("--Load {:?}", load_end - load_start);


    // //Process
    // let process_start = start.elapsed();

    // image.process();

    // let process_end = start.elapsed();
    // println!("--Process {:?}", process_end - process_start);
    

    // //Compute
    // let compute_start = start.elapsed();

    // match image.compute() {
    //     Ok(()) => println!("Image computed successfully."),
    //     Err(err) => eprintln!("Error computing image: {}", err),
    // }

    // let compute_end = start.elapsed();
    // println!("--Compute {:?}", compute_end - compute_start);

    // //info
    // image.info();

    // //Draw
    // let draw_start = start.elapsed();

    // match image.draw() {
    //     Ok(()) => println!("Image drawn successfully."),
    //     Err(err) => eprintln!("Error drawing image: {}", err),
    // }
    // let draw_end = start.elapsed();
    // println!("--Draw {:?}", draw_end  - draw_start);



    // //Save
    // let save_start = start.elapsed();

    // match image.save() {
    //     Ok(()) => println!("Image saved successfully."),
    //     Err(err) => eprintln!("Error saving image: {}", err),
    // }
    
    // let save_end = start.elapsed();
    // println!("--Save {:?}", save_end - save_start);

    // println!("--All {:?}", start.elapsed());