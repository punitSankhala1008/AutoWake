from setuptools import setup, find_packages

setup(
    name="DrowsinessDetectionApp",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A desktop application for detecting driver drowsiness using computer vision and machine learning.",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "opencv-python",
        "tensorflow",
        "dlib",
        "PyQt5",
        "numpy",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)