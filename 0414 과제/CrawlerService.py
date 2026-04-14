"""
네이버 뉴스 크롤러 서비스 (CLI)
"""
from NaverNewsCrawler import NaverNewsCrawler

CLIENT_ID = "yNtsqtpj1kGg4nHsvaTJ"
CLIENT_SECRET = "wThCv7r8yk"

def main():
    print("="*60)
    print("네이버 뉴스 크롤링 서비스")
    print("="*60)
    
    while True:
        print("\n[메뉴]")
        print("1. 뉴스 크롤링")
        print("2. 저장된 파일 목록 보기")
        print("3. 종료")
        
        choice = input("\n선택하세요 (1-3): ")
        
        if choice == '1':
            keyword = input("검색 키워드를 입력하세요: ")
            max_results = int(input("최대 수집 개수 (1000): ") or "1000")
            
            crawler = NaverNewsCrawler(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                keyword=keyword,
                max_results=max_results
            )
            
            crawler.crawl_all()
            crawler.print_summary()
            filepath = crawler.save_to_csv()
            
            print(f"\n✅ 저장 완료: {filepath}")
            
        elif choice == '2':
            import os
            if os.path.exists('./data'):
                files = os.listdir('./data')
                print("\n[저장된 파일 목록]")
                for f in files:
                    print(f"  - {f}")
            else:
                print("저장된 파일이 없습니다.")
                
        elif choice == '3':
            print("프로그램을 종료합니다.")
            break

if __name__ == "__main__":
    main()