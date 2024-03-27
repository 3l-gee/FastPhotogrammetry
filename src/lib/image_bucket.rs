use super::image::ImageStruct;
use std::collections::HashMap;
use uuid::Uuid;
use std::path::Path;
use rayon::prelude::*;

pub enum ImageBucketActions {
    Process,
    Compute,
    Save,
    Draw,
    Info,
}

#[derive(Copy, Clone)]
pub enum ProcessTypes {
    Fast,
    Default,
    Accurate,
}

pub enum ScalingFilter {
    Triangle,
    CatmullRom,
    Lanczos3,
}

pub enum AkazeType {
    Spare,
    Default,
    Dense
}

fn process_to_params(process: ProcessTypes) -> (AkazeType, f32, ScalingFilter) {
    match process {
        ProcessTypes::Fast => (AkazeType::Spare, 0.1, ScalingFilter::Triangle),
        ProcessTypes::Default => (AkazeType::Default, 0.5, ScalingFilter::CatmullRom),
        ProcessTypes::Accurate => (AkazeType::Dense, 1.0, ScalingFilter::Lanczos3),
    }
}

pub struct ImageBucketStruct {
    images: HashMap<Uuid, ImageStruct>,
    process : ProcessTypes,
    akaze_type: AkazeType,
    scaling_ratio: f32,
    scaling_filter: ScalingFilter,
}

impl ImageBucketStruct {
    pub fn new(process: ProcessTypes) -> Self {
        let (akaze_type, scaling_ratio, scaling_filter) = process_to_params(process);

        ImageBucketStruct {
            process,
            images: HashMap::new(),
            akaze_type,
            scaling_ratio,
            scaling_filter,
        }
    }

    pub fn add_image(&mut self, image: ImageStruct) {
        self.images.insert(image.id, image);
    }

    pub fn get_image(&self, id: &Uuid) -> Option<&ImageStruct> {
        self.images.get(id)
    }

    pub fn remove_image(&mut self, id: &Uuid) -> Option<ImageStruct> {
        self.images.remove(id)
    }


    pub fn add_load_images(&mut self, path: &Path, image_name_list: Vec<String>){
        for image_name in image_name_list {
            let image_name_cleaned = image_name.replace('\\', "/");  // Replace backslashes with forward slashes
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

    pub fn execute_multithreading(&mut self, action: ImageBucketActions){
        match action {
            ImageBucketActions::Process => {
                println!("Processing images in parallel:");
                self.images.par_iter_mut().for_each(|(id, image)| {
                    match image.process(self.scaling_ratio, &self.scaling_filter) {
                        Ok(()) => println!("Thread {:?}: {} processed successfully.", std::thread::current().id(), id),
                        Err(err) => eprintln!("Thread {:?}: {}, Error processing image: {}", std::thread::current().id(), id, err),
                    }
                });
            }
            ImageBucketActions::Compute => {
                println!("Computing images in parallel:");
                self.images.par_iter_mut().for_each(|(id, image)| {
                    match image.compute(&self.akaze_type) {
                        Ok(()) => println!("Thread {:?}: {} computed successfully.", std::thread::current().id(), id),
                        Err(err) => eprintln!("Thread {:?}: {}, Error computing image: {}", std::thread::current().id(), id, err),
                    }
                });
            }
            ImageBucketActions::Draw => {
                println!("Drawing images in parallel:");
                self.images.par_iter_mut().for_each(|(id, image)| {
                    match image.draw() {
                        Ok(()) => println!("-- Thread {:?}: {} drawn successfully.", std::thread::current().id(), id),
                        Err(err) => eprintln!("Thread {:?}: {}, Error drawing image: {}", std::thread::current().id(), id, err),
                    }
                });
            }
            ImageBucketActions::Save => {
                println!("Saving images in parallel:");
                self.images.par_iter_mut().for_each(|(id, image)| {
                    match image.save() {
                        Ok(()) => println!("-- Thread {:?}: {} saved successfully.", std::thread::current().id(), id),
                        Err(err) => eprintln!("Thread {:?}: {}, Error saving image: {}", std::thread::current().id(), id, err),
                    }
                });
            }
            ImageBucketActions::Info => {
                println!("Retrieving info for images in parallel:");
                self.images.par_iter().for_each(|(id, image)| {
                    image.info();
                    println!("Thread {:?}: Retrieved info for image {}.", std::thread::current().id(), id);
                });
            }
        }
    }

    pub fn execute(&mut self, action: ImageBucketActions) {
        for (id, image) in &mut self.images {
            match action {
                ImageBucketActions::Process => {
                    // Process image
                    match image.process(self.scaling_ratio, &self.scaling_filter) {         
                        Ok(()) => println!("-- {} processed successfully.", id),
                        Err(err) => eprintln!("{}, Error processing image: {}", id, err),
                    }
                }
                ImageBucketActions::Compute => {
                    // Compute on image
                    match image.compute(&self.akaze_type) {
                        Ok(()) => println!("-- {} computed successfully.", id),
                        Err(err) => eprintln!("{}, Error computing image: {}", id, err),
                    }
                }
                ImageBucketActions::Draw => {
                    // Draw on image
                    match image.draw() {
                        Ok(()) => println!("-- {} Image drawn successfully.",  id),
                        Err(err) => eprintln!("{}, Error drawing image: {}", id, err),
                    }
                }
                ImageBucketActions::Save => {
                    // Save image
                    match image.save() {
                        Ok(()) => println!("-- {} saved successfully.", id),
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

}

