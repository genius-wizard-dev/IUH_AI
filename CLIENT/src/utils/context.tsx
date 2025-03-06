import { GoogleAuthProvider, signInWithPopup, User } from "firebase/auth";
import React, { useEffect, useState } from "react";
import { auth } from "./login";
import { AuthContext, AuthContextType } from "./useAuth";

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // function signUp(email: string, password: string): any {
  //   return auth.createUserWithEmailAndPassword(email, password);
  // }

  // function logIn(email: string, password: string): any {
  //   return auth.signInWithEmailAndPassword(email, password);
  // }

  function logOut(): Promise<void> {
    return auth.signOut();
  }

  // function resetPassword(email: string): Promise<void> {
  //   return auth.sendPasswordResetEmail(email);
  // }
  const googleProvider = new GoogleAuthProvider();

  function signInWithGoogle() {
    return signInWithPopup(auth, googleProvider);
  }

  useEffect(() => {
    const unSubscribe = auth.onAuthStateChanged((user) => {
      setLoading(false);
      setCurrentUser(user as any);
    });

    return unSubscribe;
  }, []);

  const value: AuthContextType = {
    currentUser,
    // signUp,
    // logIn,
    logOut,
    // resetPassword,
    signInWithGoogle,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
