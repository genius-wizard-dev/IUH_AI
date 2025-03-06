import { User, UserCredential } from "firebase/auth";
import React from "react";
export const AuthContext = React.createContext<AuthContextType | undefined>(
  undefined
);

export interface AuthContextType {
  currentUser: User | null;
  // signUp: (email: string, password: string) => Promise<UserCredential>;
  // logIn: (email: string, password: string) => Promise<UserCredential>;
  logOut: () => Promise<void>;
  // resetPassword: (email: string) => Promise<void>;
  signInWithGoogle: () => Promise<UserCredential>;
}

export const useAuth = (): AuthContextType => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
