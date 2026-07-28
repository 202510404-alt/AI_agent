import React from 'react';
import { useState } from 'react';
import {v4 as uuidv4} from 'uuid';
import toast from 'react-hot-toast';
import {useNavigate} from "react-router-dom";
import './style.css';

function Home(){
    const navigate = useNavigate();
    
   const [uniqueId,setUniqueId] = useState("");
   const [userName,setUserName] = useState("");

   function writeId(event){
    let newId = event.target.value
    setUniqueId(newId);

  }

  function writeUserName(event){
      setUserName(event.target.value);
  }

   function generateUniqueId(event){
     event.preventDefault();
     let id = uuidv4();
     toast.success('새 보드 ID가 생성되었습니다!');
     setUniqueId(id);
    }

    function joinBoard(){
       if(!uniqueId || !userName){
        toast.error("모든 항목을 입력해 주세요");
        return;
       }
       
       navigate(`/whiteboard/${uniqueId}`, {state: {userName: userName}});
       toast.success("보드에 참가했습니다!")
    }

    return (
        <div className='home-details'>
            <div className="home-card">
                <div className="home-header">
                    <h1 className="home-title">Real-Time Canvas & Voice</h1>
                    <p className="home-subtitle">아이디어와 창의력을 자유롭게 펼쳐 보세요</p>
                </div>
                <div className="input-group">
                    <label className="input-label">보드 ID</label>
                    <input className="input" placeholder="보드 ID를 입력하세요" value={uniqueId} onChange={writeId}/>
                </div>
                <div className="input-group">
                    <label className="input-label">사용자 이름</label>
                    <input className="input" placeholder="사용자 이름을 입력하세요" value={userName} onChange={writeUserName}/>
                </div>
                <div className="button-group">
                    <button className="button button-create" onClick={generateUniqueId}>새 보드 만들기</button>
                    <button className="button button-join" onClick={joinBoard}>보드 참가</button>
                </div>
            </div>
        </div>
    );
}

export default Home;