// Base pose detector with streaming frames, when depending on the pose-detection sdk
val options = PoseDetectorOptions.Builder()
        .setDetectorMode(PoseDetectorOptions.STREAM_MODE)
        .build()

// Accurate pose detector on static images, when depending on the pose-detection-accurate sdk
val options = AccuratePoseDetectorOptions.Builder()
        .setDetectorMode(AccuratePoseDetectorOptions.SINGLE_IMAGE_MODE)
        .build()