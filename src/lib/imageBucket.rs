use super::image::ImageStruct;
use std::collections::HashMap;
use uuid::Uuid;
use std::path::Path;

#[warn(dead_code)]
pub enum ImageBucketActions {
    Process,
    Compute,
    Save,
    Draw,
    Info,
}

pub struct ImageBucketStruct {
    images: HashMap<Uuid, ImageStruct>,
}

impl ImageBucketStruct {
    pub fn new() -> Self {
        ImageBucketStruct {
            images: HashMap::new(),
        }
    }

    pub fn add_load_images(&mut self, path: &Path, image_name_list: Vec<String>){
        for image_name in image_name_list {
            let image_name_cleaned = image_name.replace("\\", "/");  // Replace backslashes with forward slashes
            let full_path = path.join(&image_name_cleaned);
            match ImageStruct::load(full_path.to_str().expect("Invalid path")) {
                Ok(image) => {
                    self.images.insert(image.id, image);
                }
                Err(err) => {
                    eprintln!("Error loading image: {}", err);
                }
            };
        }
    }

    pub fn execute(&mut self, action: ImageBucketActions) {
        for (id, image) in &mut self.images {
            match action {
                ImageBucketActions::Process => {
                    // Process image
                    image.process();
                }
                ImageBucketActions::Compute => {
                    // Compute on image
                    match image.compute() {
                        Ok(()) => println!("{} computed successfully.", id),
                        Err(err) => eprintln!("{}, Error computing image: {}", id, err),
                    }
                }
                ImageBucketActions::Draw => {
                    // Draw on image
                    match image.draw() {
                        Ok(()) => println!(" {} Image drawn successfully.",  id),
                        Err(err) => eprintln!("{}, Error drawing image: {}", id, err),
                    }
                }
                ImageBucketActions::Save => {
                    // Save image
                    match image.save() {
                        Ok(()) => println!("{} saved successfully.", id),
                        Err(err) => eprintln!("{}, Error saving image: {}", id, err),
                    }
                }
                ImageBucketActions::Info => {
                    // Save image
                    image.info()
                }
            }
        }
    }

    // pub fn add_image(&mut self, image: ImageStruct) {
    //     self.images.insert(image.id, image);
    // }
    // pub fn get_image(&self, id: &Uuid) -> Option<&ImageStruct> {
    //     self.images.get(id)
    // }

    // pub fn remove_image(&mut self, id: &Uuid) -> Option<ImageStruct> {
    //     self.images.remove(id)
    // }

    // Add more methods as needed
}