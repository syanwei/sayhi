import React from "react";
import { useRouter } from "next/router";

import { setCurrentUser } from "../util/user";

const LoginType = {
  EMAIL: 2,
  USERNAME: 1,
};

const isEmail = (email) =>
  /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/.test(
    email
  );

export default function LoginPage() {
  const router = useRouter();

  const handleLogin = async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const remember = document.getElementById("remember").checked;
    const loginType = isEmail(username) ? LoginType.EMAIL : LoginType.USERNAME;

    const rawResponse = await fetch("/api/auth/login", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: loginType === LoginType.USERNAME ? username : null,
        password,
        login_type: loginType,
        remember,
      }),
    });
    const res = await rawResponse.json();
    if (res.code === 0) {
      setCurrentUser(res.data);
      router.push("/");
    }
    alert(res.msg);
  };

  return (
    <div className="form">
      <h2>Login</h2>
      <div className="mb-3">
        <label htmlFor="username" className="form-label">
          Username / Email
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
        <label htmlFor="exampleInputPassword1" className="form-label">
          Password
        </label>
        <input type="password" className="form-control" id="password" />
      </div>
      <div className="mb-3 form-check">
        <input type="checkbox" className="form-check-input" id="remember" />
        <label className="form-check-label" htmlFor="remember">
          remember me
        </label>
      </div>
      <button className="btn btn-primary" onClick={handleLogin}>
        Login In
      </button>{" "}
      &nbsp;&nbsp;or&nbsp;&nbsp;
      <a href="#" onClick={() => router.push("/register")}>
        Register
      </a>
    </div>
  );
}
