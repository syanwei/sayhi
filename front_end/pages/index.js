import { Fragment, useEffect, useState } from "react";
import { useRouter } from "next/router";

import Comment from "../components/comment";
import { getCurrentUser, clearCurrentUser } from "../util/user";

export async function getServerSideProps({req}) {
  const res = await fetch(`http://localhost:3000/api/tree/comments`);
  const json = await res.json();

  return { props: { data: json.data, isLogin: !!req.cookies.session, } };
}


export default function Home(props) {
  const { data, isLogin } = props;
  const [username, setUsername] = useState('');
  const [isLogout, setIsLogout] = useState(false);

  const router = useRouter();

  useEffect(() => {
    setUsername(getCurrentUser()?.username ?? '');
  }, []);

  const createCommentTree = (item) =>
    <Comment item={item}>
      {item.children?.map((child) => {
        return <Fragment key={child.id}>{createCommentTree(child)}</Fragment>;
      })}
    </Comment>

  const logout = async () => {
    const res = await fetch(`http://localhost:3000/api/auth/logout`);
    const json = await res.json();
    if (json.code === 0) {
      alert("Already out!!");
    }
    if (json.code === 40004) {
      alert("You are not logged in yet!");
    }
    clearCurrentUser();
    setIsLogout(true);
    setUsername('');
  };

  return (
    <div className="container">
      <div style={{ width: "100%", textAlign: "right", display: "flex", justifyContent: "space-between" }}>
        <div>{username}</div>
        <a href="#" onClick={() => isLogin ? logout() : router.push('/login')}>
          {isLogin && !isLogout ? 'logout' : 'login'}
        </a>
      </div>
      {data.map((item, i) => {
        return <div key={i}>{createCommentTree(item)}</div>;
      })}
    </div>
  );
}
