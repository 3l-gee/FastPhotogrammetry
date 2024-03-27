#![allow(dead_code)]
#![allow(non_snake_case)]

mod lib {
    pub mod image;
    pub mod image_bucket;
}
use std::time::Instant;
use std::path::Path;

use lib::image_bucket::{ImageBucketStruct,ImageBucketActions,ProcessTypes};

fn main() { 
    let start = Instant::now();

    let path = Path::new("../../img");
    let image_name_list = vec![
        "PXL_20240317_082324792.jpg".to_string(),
        "PXL_20240317_082319750.jpg".to_string(),
        "PXL_20240317_082309262.jpg".to_string(),
        "PXL_20240317_082303565.jpg".to_string(),
        "PXL_20240317_082254819.jpg".to_string(),
        "PXL_20240317_082249759.jpg".to_string(),
        "PXL_20240317_082245096.jpg".to_string(),
        "PXL_20240317_082239261.jpg".to_string(),
        "PXL_20240317_082234839.jpg".to_string(),
        "PXL_20240317_082231220.jpg".to_string()
    ];

    {
        let mut tool = crate::ImageBucketStruct::new(ProcessTypes::Fast);

        tool.add_load_images(path, image_name_list.clone());

        tool.execute_multithreading(ImageBucketActions::Process);

        tool.execute_multithreading(ImageBucketActions::Compute);

        tool.execute_multithreading(ImageBucketActions::Draw);

        tool.execute(ImageBucketActions::Save);
    }

    println!("Execution time {:?}", start.elapsed());

}