---
applyTo: ["frontend", "ui", "react", "web-development"]
role: "frontend-developer"
description: "Prompt examples for Frontend Developer role with React and Firebase"
tags: ["react", "firebase", "cloud-run", "ui-component", "api-integration", "authentication", "deployment"]
priority: "high"
---

# **Frontend Developer: Prompt Examples (React & GCP)**

## **1. UI Component Generation**

### **Prompt**

"Generate a reusable React functional component for a user profile card using Material-UI. The component should accept a `user` object as a prop, which includes `name`, `email`, `avatarUrl`, and `bio`. The card should display the user's avatar, name, email, and a short bio. Include default prop types and basic styling."

---

## **2. API Integration (Fetching Data)**

### **Prompt**

"Write a React hook named `useUserData` that fetches user data from a Cloud Run API endpoint (`/api/users/{userId}`). The hook should handle loading, error, and data states. Use the `fetch` API and include a `userId` parameter. The hook should return an object with `{ data, isLoading, error }`."

---

## **3. Authentication Flow**

### **Prompt**

"Generate the code for a sign-in page in a React application using the Firebase Authentication SDK. The page should include form fields for email and password, a 'Sign In' button, and a 'Sign in with Google' button. Implement the `signInWithEmailAndPassword` and `signInWithPopup` (with `GoogleAuthProvider`) methods. Handle and log any authentication errors."

---

## **4. Deployment Script (CI/CD)**

### **Prompt**

"Create a `cloudbuild.yaml` file for a CI/CD pipeline that builds a React application and deploys it to Firebase Hosting. The pipeline should have two steps:
1.  **Build**: Install dependencies (`npm install`) and run the build script (`npm run build`).
2.  **Deploy**: Deploy the contents of the `build` directory to Firebase Hosting using the Firebase CLI."

---

## **5. State Management (Zustand)**

### **Prompt**

"Create a simple state management store using Zustand for a shopping cart. The store should have the following state and actions:
*   **State**: `items` (an array of product objects), `itemCount` (a number).
*   **Actions**:
    *   `addToCart(product)`: Adds a product to the cart.
    *   `removeFromCart(productId)`: Removes a product from the cart by its ID.
    *   `clearCart()`: Empties the cart.
The state should be updated correctly after each action."
