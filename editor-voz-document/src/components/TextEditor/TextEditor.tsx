import ReactQuill from 'react-quill';
import { useVoice } from '../../contexts/VoiceContext';
// import './TextEditor.styles.css';
import 'react-quill/dist/quill.snow.css';

interface TextEditorProps {
  content: string;
  onChange: (content: string) => void;
}

const modules = {
  toolbar: [
    ['bold', 'italic', 'underline', 'strike'],
    [{ 'header': [1, 2, 3, false] }],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    ['link', 'image'],
    ['clean']
  ]
};

export const TextEditor = ({ content, onChange }: TextEditorProps) => {
  const { transcript } = useVoice();

  return (
    <div className="editor-container">
      <ReactQuill
        value={content + (transcript || '')}
        onChange={onChange}
        modules={modules}
        theme="snow"
        placeholder="Comienza a escribir o usa comandos de voz..."
      />
    </div>
  );
};