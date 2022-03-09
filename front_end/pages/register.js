import React from "react";
import { useRouter } from "next/router";

export default function LoginPage(props) {
  const router = useRouter();

  const handleLogin = async () => {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const rePassword = document.getElementById("rePassword").value;

    if (password !== rePassword) {
      alert("Two inconsistent passwords");
      return;
    }

    const rawResponse = await fetch("/api/auth/signup", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, password }),
    });

    const res = await rawResponse.json();
    if (res.code === 0) {
      router.push("/login");
    }
    alert(res.msg);
  };

  return (
    <div className="form">
      <h2>Create an new Account</h2>
      <div className="mb-3">
        <label htmlFor="username" className="form-label">
          Username
        </label>
        <input
          type="text"
          className="form-control"
          id="username"
          aria-describedby="username"
          placeholder=""
        />
      </div>
      <div className="mb-3">
        <label htmlFor="email" className="form-label">
          Email
        </label>
        <input
          type="email"
          className="form-control"
          id="email"
          aria-describedby="email"
          placeholder=""
        />
      </div>
      <div className="mb-3">
        <label htmlFor="password" className="form-label">
          Password
        </label>
        <input type="password" className="form-control" id="password" />
      </div>
      <div className="mb-3">
        <label htmlFor="rePassword" className="form-label">
          Confirm Password
        </label>
        <input type="password" className="form-control" id="rePassword" />
      </div>
      <button className="btn btn-primary" onClick={handleLogin}>
        Register
      </button>
      &nbsp;&nbsp;or&nbsp;&nbsp;
      <a href="#" onClick={() => router.push("/login")}>
        Login In
      </a>
    </div>
  );
}
