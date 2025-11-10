'use client';

import { useState } from 'react';
import AudioUploader from './components/AudioUploader';
import SheetMusicDisplay from './components/SheetMusicDisplay';
import AudioPlayer from './components/AudioPlayer';

export default function Home() {
  const [transcriptionId, setTranscriptionId] = useState<string | null>(null);
  const [midiFile, setMidiFile] = useState<string | null>(null);
  const [musicXmlFile, setMusicXmlFile] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleTranscriptionComplete = (id: string, midi: string, xml?: string) => {
    setTranscriptionId(id);
    setMidiFile(midi);
    setMusicXmlFile(xml || null);
    setIsProcessing(false);
  };

  const handleReset = () => {
    setTranscriptionId(null);
    setMidiFile(null);
    setMusicXmlFile(null);
    setIsProcessing(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="border-b border-slate-200 dark:border-slate-700 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
                🎵 Audio to Sheet Music
              </h1>
              <p className="text-slate-600 dark:text-slate-400 mt-1">
                Transcribe audio files to musical notation using AI
              </p>
            </div>
            {transcriptionId && (
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors"
              >
                New Transcription
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {!transcriptionId ? (
          <div className="max-w-2xl mx-auto">
            <AudioUploader
              onTranscriptionComplete={handleTranscriptionComplete}
              isProcessing={isProcessing}
              setIsProcessing={setIsProcessing}
            />
            
            {/* Features */}
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm">
                <div className="text-3xl mb-3">🎼</div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">
                  AI-Powered
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Uses Basic Pitch by Spotify for accurate transcription
                </p>
              </div>
              <div className="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm">
                <div className="text-3xl mb-3">📝</div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">
                  Multiple Formats
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Export to MIDI and MusicXML formats
                </p>
              </div>
              <div className="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm">
                <div className="text-3xl mb-3">🎹</div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">
                  Interactive
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  View and play back your transcribed music
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Sheet Music Display */}
            {musicXmlFile && (
              <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-4">
                  Sheet Music
                </h2>
                <SheetMusicDisplay musicXmlUrl={musicXmlFile} />
              </div>
            )}

            {/* Audio Player */}
            {midiFile && (
              <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-4">
                  Playback
                </h2>
                <AudioPlayer midiUrl={midiFile} />
              </div>
            )}

            {/* Download Buttons */}
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-4">
                Download
              </h2>
              <div className="flex flex-wrap gap-4">
                {midiFile && (
                  <a
                    href={`http://localhost:8000/api/download/${transcriptionId}/midi`}
                    download
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                  >
                    Download MIDI
                  </a>
                )}
                {musicXmlFile && (
                  <a
                    href={`http://localhost:8000/api/download/${transcriptionId}/musicxml`}
                    download
                    className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
                  >
                    Download MusicXML
                  </a>
                )}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-700 mt-12 py-6">
        <div className="container mx-auto px-4 text-center text-slate-600 dark:text-slate-400 text-sm">
          <p>Powered by Basic Pitch (Spotify) • Built with Next.js & FastAPI</p>
        </div>
      </footer>
    </div>
  );
}
