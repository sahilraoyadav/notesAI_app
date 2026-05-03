import './index.css';
import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';

const API = 'http://localhost:8000';

function App(){
  const [notes,setNotes]=useState([]); const [title,setTitle]=useState(''); const [content,setContent]=useState(''); const [chatQ,setChatQ]=useState(''); const [chatA,setChatA]=useState('');
  const load=async()=>setNotes((await axios.get(`${API}/notes`)).data);
  useEffect(()=>{load();},[]);
  const create=async()=>{await axios.post(`${API}/notes`,{title,content,note_type:'text',status:'todo'});setTitle('');setContent('');load();};
  const chat=async()=>setChatA((await axios.get(`${API}/chat`,{params:{q:chatQ}})).data.answer);
  const cols=['todo','doing','done'];
  return <div className='p-6 grid gap-6'>
    <h1 className='text-2xl font-bold'>NotesAI</h1>
    <div className='grid gap-2 max-w-xl'>
      <input className='text-black p-2 rounded' placeholder='Title' value={title} onChange={e=>setTitle(e.target.value)} />
      <textarea className='text-black p-2 rounded' placeholder='Content or reminder phrase' value={content} onChange={e=>setContent(e.target.value)} />
      <button className='bg-indigo-600 px-4 py-2 rounded' onClick={create}>Add Note</button>
    </div>
    <div className='grid grid-cols-3 gap-4'>{cols.map(c=><div key={c} className='bg-slate-900 rounded p-3'><h2 className='font-semibold capitalize'>{c}</h2>{notes.filter(n=>n.status===c).map(n=><div key={n.id} className='my-2 border border-slate-700 rounded p-2'><b>{n.title}</b><p>{n.content}</p><pre className='text-xs text-slate-300'>{n.ai_summary}</pre></div>)}</div>)}</div>
    <div className='grid gap-2'>
      <h2 className='font-semibold'>Chat with your notes</h2>
      <input className='text-black p-2 rounded max-w-xl' value={chatQ} onChange={e=>setChatQ(e.target.value)} placeholder='Ask a question' />
      <button className='bg-emerald-700 px-4 py-2 rounded w-fit' onClick={chat}>Ask</button>
      <p className='whitespace-pre-wrap'>{chatA}</p>
    </div>
  </div>
}

createRoot(document.getElementById('root')).render(<App/>);
