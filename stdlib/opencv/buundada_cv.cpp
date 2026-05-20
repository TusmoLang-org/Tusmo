#include <opencv2/opencv.hpp>
#include <iostream>

extern "C" {
    // --- Sawirka (Image) ---

    void* tusmo_cv_imread(const char* filename) {
        cv::Mat* img = new cv::Mat(cv::imread(filename));
        if (img->empty()) {
            delete img;
            return nullptr;
        }
        return (void*)img;
    }

    void tusmo_cv_imshow(const char* winname, void* img_ptr) {
        if (!img_ptr) return;
        cv::Mat* img = (cv::Mat*)img_ptr;
        cv::imshow(winname, *img);
    }

    int tusmo_cv_waitKey(int delay) {
        return cv::waitKey(delay);
    }

    bool tusmo_cv_imwrite(const char* filename, void* img_ptr) {
        if (!img_ptr) return false;
        cv::Mat* img = (cv::Mat*)img_ptr;
        return cv::imwrite(filename, *img);
    }

    void tusmo_cv_destroyAllWindows() {
        cv::destroyAllWindows();
    }
    
    void tusmo_cv_freeMat(void* img_ptr) {
        if (img_ptr) {
            delete (cv::Mat*)img_ptr;
        }
    }

    // --- Camerada (VideoCapture) ---

    void* tusmo_cv_openCamera(int index) {
        cv::VideoCapture* cap = new cv::VideoCapture(index);
        if (!cap->isOpened()) {
            delete cap;
            return nullptr;
        }
        return (void*)cap;
    }

    void* tusmo_cv_readFrame(void* cap_ptr) {
        if (!cap_ptr) return nullptr;
        cv::VideoCapture* cap = (cv::VideoCapture*)cap_ptr;
        cv::Mat* frame = new cv::Mat();
        if (cap->read(*frame)) {
            return (void*)frame;
        }
        delete frame;
        return nullptr;
    }

    void tusmo_cv_releaseCamera(void* cap_ptr) {
        if (cap_ptr) {
            cv::VideoCapture* cap = (cv::VideoCapture*)cap_ptr;
            cap->release();
            delete cap;
        }
    }
}
