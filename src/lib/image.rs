use std::io::BufReader;
use std::fs::File;
use image::{self, DynamicImage};
use std::path::Path;
use uuid::Uuid;

extern crate cv;

pub struct MetadataStruct {
    pub camera : String,
    pub focal : f32
    //TODO more Metadata
}
 
pub struct DescriptorStruct {
    pub keypoints : Vec<cv::feature::akaze::KeyPoint>,
    pub descriptors : Vec<cv::bitarray::BitArray<64>>,
    pub method : String
}

pub struct ImageStruct {
    pub id : Uuid,
    pub name : String,
    pub img_raw: image::DynamicImage,
    pub img_processed: Option<image::DynamicImage>,
    pub metadata : MetadataStruct,
    pub descriptor : Option<DescriptorStruct>,
    //TODO more Image parameters
}

impl ImageStruct {
    pub fn load(path: &str) -> Result<ImageStruct, String> {
        let name = Path::new(&path).file_name().unwrap().to_str().unwrap().to_string();
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
        let metadata = MetadataStruct {
            //TODO PLACEHOLDER
            camera: String::from("Example Camera"),
            focal: 50.0,
        };

        // Create the Image struct with loaded image data and metadata
        Ok(ImageStruct {
            id: Uuid::new_v4(),
            name,
            img_raw: img,
            img_processed: None,
            metadata,
            descriptor: None
        })
    }

    pub fn info(&self) {
        println!("Image Name: {}", self.name);
        println!("Image Format: {:?}", self.img_raw.color());
        println!("Image Dimensions: {} x {}", self.img_raw.width(), self.img_raw.height());
        
        // Metadata information
        println!("Camera: {}", self.metadata.camera);
        println!("Focal Length: {}", self.metadata.focal);
        
        // Optional processed image information
        if let Some(processed_image) = &self.img_processed {
            println!("Processed Image Dimensions: {} x {}", processed_image.width(), processed_image.height());
        } else {
            println!("Processed Image: None");
        }
        
        // Descriptor information, handling the Option
        match &self.descriptor {
            Some(descriptor) => {
                println!("Descriptor Method: {}", descriptor.method);
                println!("Number of Keypoints: {}", descriptor.keypoints.len());
                println!("Number of Descriptors: {}", descriptor.descriptors.len());
            },
            None => println!("Descriptor: None"),
        }
        
        // Print more information as needed
        // For example, if you add more fields to MetadataStruct or ImageStruct,
        // add additional println! statements here following the patterns above.
    }

    pub fn process(&mut self) {
        
        match ImageStruct::scale(self.img_raw.clone()) {
            Ok(scaled_image) => {
                match ImageStruct::grayscale(scaled_image) {
                    Ok(greyscale_image) => {
                        self.img_processed = Some(greyscale_image);
                    },
                    Err(err) => eprintln!("Error grayscaling image: {}", err),
                }
            },
            Err(err) => eprintln!("Error scaling image: {}", err),
        }
    }

    pub fn compute(&mut self) -> Result<(), String> {
        let akaze = cv::feature::akaze::Akaze::default();

        // Ensure img_processed is Some; otherwise return an Err
        let image = match &self.img_processed {
            Some(image) => image,
            None => return Err("img_processed is None".to_string()),
        };

        // Proceed with the computation since we now have an image
        let (keypoints, descriptors) = akaze.extract(image);

        let descriptor = DescriptorStruct {
            keypoints,
            descriptors,
            method: "AKAZE".to_string(),
        };
        self.descriptor = Some(descriptor);

        Ok(())
    }

    fn grayscale(image: DynamicImage) -> Result<DynamicImage, image::ImageError> {
        Ok(image.grayscale())
    }

    fn scale(image: DynamicImage) -> Result<DynamicImage, image::ImageError> {
        let ratio = 0.5;
        let original_width = image.width();
        let original_height = image.height();
    
        // Calculate new dimensions based on the provided ratio
        let new_width = (original_width as f32 * ratio) as u32;
        let new_height = (original_height as f32 * ratio) as u32;
    
        // Resize the image using the new dimensions
        Ok(image.resize(new_width, new_height, image::imageops::FilterType::Triangle))
    }

    pub fn draw(&mut self) -> Result<(), String> {  
        let descriptor = match &self.descriptor {
            Some(descriptor) => descriptor,
            None => return Err("descriptor is None".to_string()),
        };

        let image = match &self.img_processed {
            Some(image) => image,
            None => return Err("img_processed is None".to_string()),
        };

        let mut image_canvas = cv::image::imageproc::drawing::Blend(image.to_rgba8());

        for keypoint in &descriptor.keypoints {
            let (x, y) = (keypoint.point.0 as i32, keypoint.point.1 as i32);
            cv::image::imageproc::drawing::draw_cross_mut(
                &mut image_canvas,
                image::Rgba([0, 255, 255, 128]),
                x,
                y,
            );
            
        }
        let out_image = DynamicImage::ImageRgba8(image_canvas.0);

        self.img_processed = Some(out_image);

        Ok(())
    }


    pub fn save(&self) -> Result<(), String> {
        let output_name = self.name.clone();
        output_name.splitn(2, ".").next().unwrap_or("");
        let output_path = Path::new("C:/Users/Raphael_Gerth/Documents/HOME/FUNTIMES_Rust/photogrametry/output").join(output_name).with_extension("png");
        println!("Image saved at {}", output_path.display());
        match &self.img_processed {
            Some(image) => {
                match image.save_with_format(output_path, image::ImageFormat::Png) {
                    Ok(_) => Ok(()),
                    Err(e) => Err(format!("Failed to save image : {}", e)),
                }

            },
            None => Err("img_processed is None".to_string()),
        }
    }
}

