# run.py

from app.converter.src import convert

def main():
    python_file = './app/converter/test/example.py'
    cpp_file = './app/converter/test/output.cpp'
    
    convert(python_file, cpp_file)
    print(f"Conversion completed. Saved in {cpp_file}")

if __name__ == "__main__":
    main()
