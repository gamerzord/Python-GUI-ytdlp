import os
import subprocess
from typing import List, Dict, Any


class CommandBuilder:
    """Builds yt-dlp commands based on user options"""
    
    def __init__(self):
        self.ytdlp_cmd = 'yt-dlp'
    
    def check_installation(self) -> bool:
        """Check if yt-dlp is installed"""
        try:
            result = subprocess.run([self.ytdlp_cmd, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def get_version(self) -> str:
        """Get yt-dlp version"""
        try:
            result = subprocess.run([self.ytdlp_cmd, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return result.stdout.strip()
            return "Unknown"
        except:
            return "Unknown"
    
    def build_download_command(self, options: Dict[str, Any]) -> List[str]:
        """Build download command from options"""
        url = options.get('url', '').strip()
        if not url:
            raise ValueError("URL is required")
        
        cmd = [self.ytdlp_cmd]
        
        # Output path
        output_path = os.path.join(options.get('output_path', '.'), '%(title)s.%(ext)s')
        cmd.extend(['-o', output_path])
        
        # Format selection
        if options.get('audio_only', False):
            audio_format = options.get('audio_format', 'best')
            if audio_format != "best":
                cmd.extend(['-f', 'bestaudio', '--extract-audio', '--audio-format', audio_format])
                audio_quality = options.get('audio_quality', 'best')
                if audio_quality != "best":
                    cmd.extend(['--audio-quality', audio_quality])
            else:
                cmd.extend(['-f', 'bestaudio', '--extract-audio'])
        else:
            format_str = options.get('format', 'best')
            quality = options.get('quality', 'best')
            
            if quality != "best" and quality.endswith('p'):
                height = quality[:-1]
                format_str = f"best[height<={height}]"
            
            cmd.extend(['-f', format_str])
        
        # Subtitles
        if options.get('subtitle', False):
            cmd.extend(['--write-subs', '--write-auto-subs'])
            if options.get('embed_subs', False):
                cmd.append('--embed-subs')
        
        # Thumbnail
        if options.get('write_thumbnail', False):
            cmd.append('--write-thumbnail')
        
        # Playlist
        if not options.get('playlist', False):
            cmd.append('--no-playlist')
        
        # SponsorBlock
        if options.get('sponsorblock', False):
            categories = options.get('sponsor_categories', 'sponsor,selfpromo')
            cmd.extend(['--sponsorblock-remove', categories])
        
        # Custom arguments
        custom_args = options.get('custom_args', '').strip()
        if custom_args:
            cmd.extend(custom_args.split())
        
        cmd.append(url)
        return cmd
    
    def build_info_command(self, options: Dict[str, Any]) -> List[str]:
        """Build info command from options"""
        url = options.get('url', '').strip()
        if not url:
            raise ValueError("URL is required")
        
        cmd = [self.ytdlp_cmd, '--dump-json', '--no-download']
        
        # Custom arguments (if any apply to info gathering)
        custom_args = options.get('custom_args', '').strip()
        if custom_args:
            # Filter out download-specific args that might conflict
            safe_args = []
            args_list = custom_args.split()
            skip_next = False
            
            download_specific_args = {
                '-o', '--output', '-f', '--format', '--extract-audio',
                '--audio-format', '--audio-quality', '--write-subs',
                '--embed-subs', '--write-thumbnail', '--sponsorblock-remove'
            }
            
            for i, arg in enumerate(args_list):
                if skip_next:
                    skip_next = False
                    continue
                
                if arg in download_specific_args:
                    # Skip this arg and potentially the next one (if it's a value)
                    if i + 1 < len(args_list) and not args_list[i + 1].startswith('-'):
                        skip_next = True
                    continue
                
                safe_args.append(arg)
            
            if safe_args:
                cmd.extend(safe_args)
        
        cmd.append(url)
        return cmd
    
    def validate_url(self, url: str) -> bool:
        """Basic URL validation"""
        if not url.strip():
            return False
        
        # Basic URL patterns
        valid_patterns = [
            'http://', 'https://',
            'youtube.com', 'youtu.be',
            'twitch.tv', 'twitter.com',
            'instagram.com', 'tiktok.com'
        ]
        
        url_lower = url.lower()
        return any(pattern in url_lower for pattern in valid_patterns)
    
    def get_supported_sites(self) -> List[str]:
        """Get list of supported sites from yt-dlp"""
        try:
            result = subprocess.run([self.ytdlp_cmd, '--list-extractors'], 
                                  capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                sites = result.stdout.strip().split('\n')
                return [site.strip() for site in sites if site.strip()]
            return []
        except:
            return []
    
    def test_url(self, url: str) -> Dict[str, Any]:
        """Test if URL is valid and accessible"""
        try:
            cmd = [self.ytdlp_cmd, '--simulate', '--quiet', url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            return {
                'valid': result.returncode == 0,
                'error': result.stderr if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {'valid': False, 'error': 'Timeout while testing URL'}
        except Exception as e:
            return {'valid': False, 'error': str(e)}