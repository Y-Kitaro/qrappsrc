import React, { useState } from 'react';
import './App.css';

// 各タブの内容を描画するコンポーネント
const TabContent = ({ activeTab }) => {
  // =================================================================
  // Tab 1: 単一QRコード作成
  // =================================================================
  const [inputText, setInputText] = useState('');
  const [qrCodeImage, setQrCodeImage] = useState('');
  const [makeLoading, setMakeLoading] = useState(false);
  const [makeError, setMakeError] = useState('');
  const [version, setVersion] = useState(10);
  const [errorCorrection, setErrorCorrection] = useState('L');

  const handleGenerateQrCode = async () => {
    if (!inputText.trim()) {
      setMakeError('QRコードに変換するテキストを入力してください。');
      setQrCodeImage('');
      return;
    }
    setMakeLoading(true);
    setMakeError('');
    setQrCodeImage('');

    try {
      if (window.pywebview && window.pywebview.api.qrcode_utils.make_qrcode_base64) {
        const imageData = await window.pywebview.api.qrcode_utils.make_qrcode_base64(
          inputText, Number(version), errorCorrection
        );
        if (imageData.startsWith("data:image/png;base64,")) {
          setQrCodeImage(imageData);
        } else {
          // Python側でエラーメッセージが返ってきた場合
          setMakeError(imageData);
        }
      } else {
        setMakeError('Pywebview API (make_qrcode_base64) が見つかりません。');
      }
    } catch (err) {
      setMakeError(`QRコードの生成に失敗しました: ${err.message || String(err)}`);
    } finally {
      setMakeLoading(false);
    }
  };

  // =================================================================
  // Tab 2: 一括作成
  // =================================================================
  const [bulkStatus, setBulkStatus] = useState('');
  const [bulkLoading, setBulkLoading] = useState(false);
  const [qrcodeCsvFile, setQrcodeCsvFile] = useState('');
  const [qrcodeSaveDir, setQrcodeSaveDir] = useState('');

  const hanldeSetQrcodeCsvFile = async () => {
    setQrcodeCsvFile('');
    try {
      if (window.pywebview && window.pywebview.api.open_file) {
        const qrCodeCsvFile = await window.pywebview.api.open_file(['CSV files (*.csv)', 'All files (*.*)'], false);
        setQrcodeCsvFile(qrCodeCsvFile);
      }
    } catch (err) {
    } finally {
    }
  }

  const handleSetQrCodeSaveDir = async () => {
    setQrcodeSaveDir('');
    try {
      if (window.pywebview && window.pywebview.api.select_folder) {
        const qrCodeSaveDir = await window.pywebview.api.select_folder();
        setQrcodeSaveDir(qrCodeSaveDir);
      }
    } catch (err) {
    } finally {
    }
  }

  const handleSelectCsvAndFolder = async () => {
    setBulkLoading(true);
    setBulkStatus('');

    try {
        if (!window.pywebview || !window.pywebview.api.qrcode_utils.make_qrcode_csv) {
            setBulkStatus('Pywebview API (make_qrcode_csv) が見つかりません。');
            setBulkLoading(false);
            return;
        }

        setBulkStatus(`処理中... CSV: ${qrcodeCsvFile}, 出力先: ${qrcodeSaveDir}`);

        // Pythonの関数を呼び出す
        const result = await window.pywebview.api.qrcode_utils.make_qrcode_csv(qrcodeCsvFile, qrcodeSaveDir);
        setBulkStatus(`処理結果: ${result}`);

    } catch (err) {
        setBulkStatus(`一括作成中にエラーが発生しました: ${err.message || String(err)}`);
    } finally {
        setBulkLoading(false);
    }
  };

  // =================================================================
  // Tab 3: デコード
  // =================================================================
  const [decodedText, setDecodedText] = useState('');
  const [decodeLoading, setDecodeLoading] = useState(false);
  const [decodeStatus, setDecodeStatus] = useState('');

  const handleDecodeQrCode = async () => {
    setDecodeLoading(true);
    setDecodedText('');
    setDecodeStatus('');

    try {
      if (!window.pywebview || !window.pywebview.api.qrcode_utils.decode_qrcode) {
        setDecodeStatus('Pywebview API (decode_qrcode) が見つかりません。');
        setDecodeLoading(false);
        return;
      }
      
      // 画像ファイルを選択させる
      const result = await window.pywebview.api.qrcode_utils.decode_qrcode();
      if (result.startsWith("Error")) {
          setDecodeStatus(result);
      } else {
          setDecodedText(result);
          setDecodeStatus('デコードに成功しました。');
      }

    } catch (err) {
      setDecodeStatus(`デコード中にエラーが発生しました: ${err.message || String(err)}`);
    } finally {
      setDecodeLoading(false);
    }
  };


  // =================================================================
  // タブごとの描画内容
  // =================================================================
  if (activeTab === 'create') {
    return (
      <div className="tab-pane">
        <div className="form-container">
          <fieldset className="options-fieldset">
            <legend>QRCodeオプション</legend>
            <div className="form-group-inline">
                <label htmlFor="qr-version">バージョン:</label><input id="qr-version" type="number" value={version} min="1" max="40" onChange={(e) => setVersion(e.target.value)} />
                <label htmlFor="qr-error-correction">誤り訂正レベル:</label><select id="qr-error-correction" value={errorCorrection} onChange={(e) => setErrorCorrection(e.target.value)}><option value="L">L</option><option value="M">M</option><option value="Q">Q</option><option value="H">H</option></select>
            </div>
          </fieldset>
          <div className="form-group">
            <label htmlFor="qr-text">QRコードテキスト:</label>
            <textarea id="qr-text" value={inputText} onChange={(e) => setInputText(e.target.value)} rows={3} placeholder="Enter text here" />
          </div>
          <button onClick={handleGenerateQrCode} disabled={makeLoading}>{makeLoading ? '作成中...' : 'QRコードを作成'}</button>
        </div>
        {makeError && <p className="status-message">{makeError}</p>}
        {qrCodeImage && (
          <img src={qrCodeImage} alt="Generated QR Code" className="qrcode-result"/>
        )}
      </div>
    );
  }

  if (activeTab === 'bulk') {
    return (
      <div className="tab-pane">
        <p>CSVファイルと、QRコード画像の保存先フォルダを選択してください。</p>
        <div className="form-container">
            <div className="form-group-inline">
                {<p className="status-message">{qrcodeCsvFile}</p>}
                <button onClick={hanldeSetQrcodeCsvFile} disabled={bulkLoading}>{bulkLoading ? '処理中...' : 'CSVを選択'}</button>
            </div>
        </div>
        <div className="form-container">
            <div className="form-group-inline">
                {<p className="status-message">{qrcodeSaveDir}</p>}
                <button onClick={handleSetQrCodeSaveDir} disabled={bulkLoading}>{bulkLoading ? '処理中...' : '保存先を選択'}</button>
            </div>
        </div>
        <div className="form-container">
              <button onClick={handleSelectCsvAndFolder} disabled={bulkLoading}>{bulkLoading ? '処理中...' : 'QRコード作成を開始'}</button>
        </div>
        {bulkStatus && <p className="status-message">{bulkStatus}</p>}
      </div>
    );
  }

  if (activeTab === 'decode') {
    return (
        <div className="tab-pane">
            <p>デコードしたいQRコード画像ファイルを選択してください。</p>
            <div className="form-container">
                <button onClick={handleDecodeQrCode} disabled={decodeLoading}>{decodeLoading ? 'デコード中...' : '画像ファイルを選択'}</button>
            </div>
            {decodeStatus && <p className="status-message">{decodeStatus}</p>}
            {decodedText && (
                <div className="form-group">
                  <label htmlFor="qr-text">デコード結果:</label>
                  <textarea>{decodedText}</textarea>
                </div>
            )}
        </div>
    );
  }

  return null;
};

// メインのAppコンポーネント
function App() {
  const [activeTab, setActiveTab] = useState('create');

  return (
    <div className="App">
      <header className="App-header">
        <h1>QR Code ツール</h1>
      </header>
      <nav className="tab-nav">
        <button onClick={() => setActiveTab('create')} className={activeTab === 'create' ? 'active' : ''}>作成</button>
        <button onClick={() => setActiveTab('bulk')} className={activeTab === 'bulk' ? 'active' : ''}>一括作成</button>
        <button onClick={() => setActiveTab('decode')} className={activeTab === 'decode' ? 'active' : ''}>デコード</button>
      </nav>
      <main className="tab-content">
        <TabContent activeTab={activeTab} />
      </main>
    </div>
  );
}

export default App;