import React, { useState } from "react";
import { FaFile } from "react-icons/fa";
import { LiaSearchSolid } from "react-icons/lia";
import { IoIosSettings } from "react-icons/io";
import { AiFillThunderbolt } from "react-icons/ai";
import { LiaSpiderSolid } from "react-icons/lia";
import { BsBoxSeam } from "react-icons/bs";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";

const Sidebar = () => {
  // 현재 활성 탭 상태를 관리 (초기값은 "case")
  const [activeTab, setActiveTab] = useState("case");
  const [openModal, setOpenModal] = useState(false);

  // 각 탭에 따른 사이드바 내용을 조건부로 렌더링하는 함수
  const renderContent = () => {
    switch (activeTab) {
      case "case":
        return <div>Case Content</div>;
      case "source":
        return <div>Source Content</div>;
      case "search":
        return <div>Search Content</div>;
      case "process":
        return <div>Process Content</div>;
      case "TTP Mapping":
        return <div>TTP Mapping Content</div>;
      case "settings":
        return <div>Settings Content</div>;
      default:
        return <div>Content Not Found</div>;
    }
  };

  return (
    <div className="sidebar-section">
      <div className="icon-list">
        <div>
          {/* 첫 번째 아이콘: case */}
          <div
            className={`icon ${activeTab === "case" ? "active" : ""}`}
            onClick={() => setActiveTab("case")}
            style={{ cursor: "pointer" }}
          >
            <BsBoxSeam />
          </div>
          {/* 두 번째 아이콘: source */}
          <div
            className={`icon ${activeTab === "source" ? "active" : ""}`}
            onClick={() => setActiveTab("source")}
            style={{ cursor: "pointer" }}
          >
            <FaFile />
          </div>
          {/* 세 번째 아이콘: search */}
          <div
            className={`icon ${activeTab === "search" ? "active" : ""}`}
            onClick={() => setActiveTab("search")}
            style={{ cursor: "pointer" }}
          >
            <LiaSearchSolid />
          </div>
          {/* 네 번째 아이콘: process */}
          <div
            className={`icon ${activeTab === "process" ? "active" : ""}`}
            onClick={() => setActiveTab("process")}
            style={{ cursor: "pointer" }}
          >
            <LiaSpiderSolid />
          </div>
          {/* 다섯 번째 아이콘: TTP Mapping */}
          <div
            className={`icon ${activeTab === "TTP Mapping" ? "active" : ""}`}
            onClick={() => setActiveTab("TTP Mapping")}
            style={{ cursor: "pointer" }}
          >
            <AiFillThunderbolt />
          </div>
        </div>
        <div>
          {/* 여섯 번째 아이콘: settings */}
          <div
            className="icon"
            onClick={() => {
              setActiveTab("settings");
              setOpenModal(true);
            }}
            style={{ cursor: "pointer" }}
          >
            <IoIosSettings />
          </div>
        </div>
      </div>

      {/* settings 탭이 아닌 경우에만 explorer-list에 내용을 보여줌 */}
      <div className="explorer-list">
        {activeTab !== "settings" && renderContent()}
      </div>

      {/* MUI Dialog: settings 클릭 시 모달이 열림 */}
      <Dialog open={openModal} onClose={() => setOpenModal(false)}>
        <DialogTitle>Settings</DialogTitle>
        <DialogContent>Settings Content</DialogContent>
        <DialogActions>
          <Button
            onClick={() => setOpenModal(false)}
            color="primary"
            variant="contained"
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default Sidebar;
