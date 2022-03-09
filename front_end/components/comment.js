import { useState } from "react";
import dayjs from "dayjs";
import {
  BsFillCaretDownFill,
  BsFillCaretRightFill,
  BsXLg,
} from "react-icons/bs";

import PublishBox from "./publishBox";

const Comment = ({ item, children }) => {
  const [showChildren, setShowChildren] = useState(false);
  const [showPublishPanel, setShowPublishPanel] = useState(false);

  return (
    <div>
      <div className="comment">
        <div
          className="comment-icon"
          onClick={() => setShowChildren(!showChildren)}
        >
          {showChildren ? <BsFillCaretDownFill /> : <BsFillCaretRightFill />}
        </div>
        <div>
          <h3 className="comment-title">{item.username}</h3>
          <label className="comment-time">
            {dayjs(item.created_at).format("YYYY-MM-DD HH:mm:ss")}
          </label>
          <div className="comment-content">
            <div onClick={() => setShowPublishPanel(true)}>{item.comment}</div>
          </div>
        </div>
      </div>
      {showPublishPanel ? (
        <div className="comment-reply">
          <PublishBox
            replyTo={item.username}
            parentId={item.id}
            handleClose={() => setShowPublishPanel(false)}
          />
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={() => setShowPublishPanel(false)}
          >
            <BsXLg />
          </button>
        </div>
      ) : (
        ""
      )}

      <div className="comment-children">{showChildren && children}</div>
    </div>
  );
};

export default Comment;
