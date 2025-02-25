import React from "react";
import Sidebar from "../components/sections/Sidebar";
import Content from "../components/sections/Content";

const Main = () => {
  return (
    <div className="wrapper-component">
      <div className="header-section"></div>
      <div className="middle-section">
        <Sidebar />
        <Content />
      </div>
      <div className="footer-section"></div>
    </div>
  );
};

export default Main;
