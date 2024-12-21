import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
from database import create_db, insert_sample_products, get_products, add_to_cart, add_review

class ECommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Store E-Commerce Platform")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f8ff")  # Light blue background

        # Ensure the database and tables are created
        create_db()

        # Insert sample products if they don't exist
        insert_sample_products()

        # Create product listing
        self.create_product_listing()

    def create_product_listing(self):
        # Fetch products from the database
        products = get_products()

        # Check if products are fetched
        if not products:
            messagebox.showinfo("No Products", "No products found in the database.")
            return

        # Create a frame for product listing
        product_frame = tk.Frame(self.root, bg="#f0f8ff")
        product_frame.pack(pady=20)

        for i, product in enumerate(products):
            product_id, name, description, price, image = product

            # Try to load the product image
            try:
                image_path = os.path.join(os.getcwd(), image)
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    img = img.resize((100, 100))
                    img = ImageTk.PhotoImage(img)
                else:
                    raise FileNotFoundError(f"Image {image} not found.")
            except Exception as e:
                print(f"Error loading image for product {product_id}: {e}")
                img = Image.new('RGB', (100, 100), color='gray')
                img = ImageTk.PhotoImage(img)

            panel = tk.Label(product_frame, image=img, bg="#f0f8ff")
            panel.image = img  # Keep a reference to prevent garbage collection
            panel.grid(row=i, column=0, padx=10, pady=10)

            # Product name and description
            name_label = tk.Label(product_frame, text=name, font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#333333")
            name_label.grid(row=i, column=1, sticky="w")

            description_label = tk.Label(product_frame, text=description, wraplength=200, bg="#f0f8ff", fg="#555555")
            description_label.grid(row=i, column=2, sticky="w")

            price_label = tk.Label(product_frame, text=f"${price:.2f}", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#ff4500")
            price_label.grid(row=i, column=3, sticky="w")

            # Add to cart button
            add_to_cart_button = tk.Button(product_frame, text="Add to Cart", bg="#32cd32", fg="white", font=("Arial", 10, "bold"), command=lambda p_id=product_id: self.add_to_cart(p_id))
            add_to_cart_button.grid(row=i, column=4, padx=5)

            # Review button
            review_button = tk.Button(product_frame, text="Write Review", bg="#1e90ff", fg="white", font=("Arial", 10, "bold"), command=lambda p_id=product_id: self.write_review(p_id))
            review_button.grid(row=i, column=5, padx=5)

    def add_to_cart(self, product_id):
        add_to_cart(product_id, 1)  # Add product with quantity 1
        messagebox.showinfo("Cart", f"Product {product_id} added to the cart!")

    def write_review(self, product_id):
        review_window = tk.Toplevel(self.root)
        review_window.title("Write Review")
        review_window.configure(bg="#f0f8ff")

        user_label = tk.Label(review_window, text="Your Name:", bg="#f0f8ff", fg="#333333")
        user_label.pack(pady=5)
        user_entry = tk.Entry(review_window)
        user_entry.pack(pady=5)

        review_label = tk.Label(review_window, text="Your Review:", bg="#f0f8ff", fg="#333333")
        review_label.pack(pady=5)
        review_text = tk.Text(review_window, height=5, width=40)
        review_text.pack(pady=5)

        def submit_review():
            user_name = user_entry.get()
            review_content = review_text.get("1.0", "end-1c")
            add_review(product_id, user_name, review_content)
            messagebox.showinfo("Review", "Review submitted successfully!")
            review_window.destroy()

        submit_button = tk.Button(review_window, text="Submit Review", bg="#32cd32", fg="white", font=("Arial", 10, "bold"), command=submit_review)
        submit_button.pack(pady=10)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ECommerceApp(root)
    root.mainloop()
