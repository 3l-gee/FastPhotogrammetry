mod lib {
    pub mod image;
}

use lib::image::{Image, ImageProcessing};

fn main() {
    // Load an image
    let image_path = "img/PXL_20240317_082231220.jpg"; // Replace with the actual path to your image file
    let image = match crate::Image::load(image_path) {
        Ok(image) => image,
        Err(err) => {
            eprintln!("Error loading image: {}", err);
            return;
        }
    };

    image.save()
}