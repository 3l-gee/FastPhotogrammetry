use std::io::BufReader;
use std::fs::File;
use image;

pub struct Metadata {
    pub camera : String,
    pub focal : f32
    //TODO more Metadata
}

pub struct Image {
    pub name : String,
    pub img: image::DynamicImage,
    pub metadata : Metadata
    //TODO more Image parameters
}

pub trait ImageProcessing {
    fn load(path: &str) -> Result<Image, String>;
    fn save(&self);
}

impl ImageProcessing for Image {
    fn load(path: &str) -> Result<Image, String> {
        // Load the image from the specified file path
        let file = match File::open(path) {
            Ok(file) => file,
            Err(err) => return Err(format!("Failed to open image file: {}", err)),
        };

        let reader = BufReader::new(file);
        let format = match image::ImageFormat::from_path(path) {
            Ok(format) => format,
            Err(err) => return Err(format!("Failed to find the image format: {}", err)),
        };

        let img = match image::load(reader,    format) {
            Ok(img) => img,
            Err(err) => return Err(format!("Failed to decode image: {}", err)),
        };

        // Extract image metadata
        let metadata = Metadata {
            //TODO PLACEHOLDER
            camera: String::from("Example Camera"),
            focal: 50.0,
        };

        // Create the Image struct with loaded image data and metadata
        Ok(Image {
            name: String::from("Example Image"),
            img,
            metadata,
        })
    }
    
    fn save(&self) {
        // Save the image
        let _ =image::DynamicImage::save_with_format(&self.img, "C:/Users/Raphael_Gerth/Downloads", image::ImageFormat::Png);

    }
}

