import { useRouter } from "next/router";

const PublishBox = ({ replyTo, parentId, handleClose }) => {
  const router = useRouter();

  const publish = async () => {
    const rawResponse = await fetch("/api/tree/comment", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        comment: document.getElementById(`input-${parentId}`).value,
        parent_id: parentId,
      }),
    });
    const res = await rawResponse.json();

    if (res.code === 40004) {
      alert("You need to login before publish comment");
      router.push("/login");
    }

    handleClose();
  };

  return (
    <div className="input-group">
      <input
        type="text"
        id={`input-${parentId}`}
        className="form-control"
        placeholder={`reply to ${replyTo}`}
        aria-label={`reply to ${replyTo}`}
        aria-describedby="basic-addon2"
      />
      <span
        className="input-group-text"
        id="basic-addon2"
        style={{ cursor: "pointer" }}
        onClick={() => publish()}
      >
        Reply
      </span>
    </div>
  );
};

export default PublishBox;
