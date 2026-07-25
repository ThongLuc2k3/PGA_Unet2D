# Ôn tập phản biện bảo vệ khóa luận

Tài liệu này gộp lại từ 3 bản ôn thi trước đó (10 câu hỏi hội đồng khó tính, 15 câu phản biện miệng, 30 câu bám sát report), đã bỏ trùng lặp và sắp xếp lại theo chủ đề. Mỗi câu trả lời viết theo hướng ngắn, chắc, nói được trong khoảng 20-30 giây, tránh trả lời lan man. Đọc ý chính trước, không cần học thuộc từng chữ.

---

## A. Phạm vi bài toán và đóng góp

**1. Vì sao chọn bài toán phân đoạn có câu nhắc thay vì phân đoạn tự động hoàn toàn?**

Vì với ảnh X-quang xương, tổn thương thường nhỏ, biên không rõ và dễ bị chồng lấp bởi cấu trúc giải phẫu khác. Nếu bắt mô hình vừa tự tìm vừa tự phân đoạn thì yêu cầu khả năng cao hơn hẳn. Hướng có câu nhắc nằm ở giữa: người dùng khoanh sơ bộ vùng nghi ngờ, còn mô hình làm phần phân đoạn chi tiết. Cách này hợp hơn với một hệ hỗ trợ, chứ không phải một hệ chẩn đoán tự động hoàn toàn.

**2. Đóng góp chính của khóa luận là gì?**

Có ba phần cốt lõi. Một là biểu diễn hộp giới hạn bằng bản đồ nhiệt dạng cao nguyên, có làm mềm biên bằng Gaussian. Hai là đưa câu nhắc vào bộ mã hóa qua PSG. Ba là đưa thông tin câu nhắc vào nhánh giải mã qua CAD. Ba thành phần này có tác dụng rõ hơn khi đi cùng nhau. Ngoài ra khóa luận còn có một thử nghiệm mở rộng với Gatekeeper, nhưng đó không phải đóng góp kiến trúc chính.

**3. Điểm mới của PGA-UNet so với U-Net hoặc Attention U-Net là gì?**

U-Net gốc không nhận câu nhắc. Attention U-Net có cổng chú ý nhưng vẫn không dùng trực tiếp thông tin định hướng từ người dùng. PGA-UNet khác ở chỗ nó không chỉ ghép câu nhắc ở đầu vào, mà duy trì ảnh hưởng của câu nhắc xuyên suốt cả bộ mã hóa và bộ giải mã, thông qua PSG và CAD.

**4. Nếu hội đồng hỏi thẳng: "Khóa luận này mới ở mức mô phỏng, vậy giá trị khoa học và giá trị ứng dụng của nó là gì?"**

Em sẽ tách hai phần. Về giá trị khoa học, khóa luận đề xuất và kiểm tra một cách tích hợp câu nhắc xuyên suốt cả bộ mã hóa và bộ giải mã, trong đó bằng chứng rõ nhất là khả năng giữ hiệu năng khi câu nhắc bị sai lệch. Về giá trị ứng dụng, em không nói đây là hệ thống sẵn sàng lâm sàng. Giá trị ứng dụng hiện tại nằm ở chỗ nó chỉ ra một hướng thiết kế gọn nhẹ, phản hồi nhanh, và có tiềm năng cho bài toán hỗ trợ nếu sau này được kiểm tra với người dùng thật và dữ liệu ngoài.

---

## B. Công bằng trong so sánh

**5. So sánh với U-Net và Attention U-Net không cùng điều kiện đầu vào (PGA-UNet có câu nhắc, hai mô hình kia không), vậy đưa kết quả đó vào phần chính có công bằng không?**

Đây không phải phép so sánh cùng điều kiện đầu vào, và khóa luận nói rõ điều này. Mục đích của so sánh là thể hiện lợi ích tổng thể của thiết lập phân đoạn có hướng dẫn bằng câu nhắc so với mô hình tự động, không dùng để khẳng định riêng tính mới của kiến trúc. Phần đánh giá đóng góp kiến trúc công bằng hơn nằm ở ablation, nơi các cấu hình như U-Net+Concat, U-Net+PSG, U-Net+CAD và PGA-UNet đều cùng nhận câu nhắc.

**6. Nếu vậy, đóng góp của PGA-UNet có đang bị trộn lẫn với lợi ích của việc có câu nhắc không?**

Nếu chỉ nhìn vào so sánh với U-Net và Attention U-Net thì có thể bị trộn lẫn, nên khóa luận mới tách riêng phần ablation. Ở đó, U-Net+Concat, U-Net+PSG, U-Net+CAD và PGA-UNet đều cùng nhận câu nhắc. Từ phần này mới rút ra được rằng lợi ích nhất quán nhất của thiết kế nằm ở CAD và Gaussian trong kịch bản Lệch tâm, chứ không chỉ vì "có hộp giới hạn".

**7. Vì sao chọn SAM-Med2D làm mô hình đối sánh chính?**

Vì SAM-Med2D là mô hình nền tảng có hỗ trợ câu nhắc và đã được thích nghi cho ảnh y khoa 2D. Nó phù hợp hơn với bối cảnh dữ liệu của khóa luận, đồng thời cho phép đối sánh trong cùng bối cảnh đầu vào là hộp giới hạn.

**8. So sánh với SAM-Med2D có công bằng không khi hai mô hình được đánh giá ở độ phân giải khác nhau?**

Khóa luận xử lý điểm này bằng cách huấn luyện lại PGA-UNet ở 256×256 để so sánh cùng độ phân giải với SAM-Med2D. Vì vậy, kết luận so sánh trực tiếp giữa hai hệ thống chủ yếu dựa trên kết quả ở 256×256, không lẫn với kết quả ở 512×512.

**9. So sánh với SAM-Med2D có thật sự cho thấy PGA-UNet tốt hơn, hay chỉ cho thấy mô hình nhẹ hơn thì hợp bộ dữ liệu nhỏ hơn?**

Em nghĩ kết quả hiện tại chỉ cho phép kết luận trong phạm vi thực nghiệm: ở cùng đầu vào hộp giới hạn và cùng độ phân giải 256×256, PGA-UNet cho kết quả cao hơn SAM-Med2D trên cả hai bộ dữ liệu này. Em không mở rộng thành kết luận chung rằng CNN nhẹ hơn luôn tốt hơn mô hình nền tảng. Dữ liệu và bối cảnh này có thể phù hợp hơn với một mô hình gọn nhẹ, dễ huấn luyện từ đầu và dễ kiểm soát hơn.

---

## C. Dữ liệu và thiết lập thực nghiệm

**10. Vì sao dùng cả BTXRD và FracAtlas?**

Vì hai bộ dữ liệu này khác nhau về dạng tổn thương. BTXRD là khối u xương, còn FracAtlas là gãy xương. Dùng cả hai giúp kiểm tra xem thiết kế có chỉ hợp với một kiểu tổn thương hay không.

**11. Bạn chia tập dữ liệu thế nào? Có nguy cơ rò rỉ dữ liệu (leakage) không?**

Việc chia tập được thực hiện ở cấp độ ảnh, tức các đa giác thuộc cùng một ảnh luôn nằm trong cùng một tập, nên tránh được rò rỉ ở cấp độ vùng tổn thương. Tuy nhiên, khóa luận chưa xác nhận được ở cấp độ bệnh nhân, vì siêu dữ liệu công khai không cung cấp mã định danh bệnh nhân đầy đủ. Đây là một hạn chế thật sự và đã được nêu rõ trong report; em không cố gắng biện hộ cho điều này.

**12. Câu nhắc trong thực nghiệm được lấy từ đâu? Việc tạo câu nhắc từ nhãn gốc có làm kết quả đẹp hơn thực tế không?**

Câu nhắc được tạo từ nhãn gốc dưới dạng hộp giới hạn, sau đó biến đổi theo ba kịch bản Bao trọn, Lệch tâm và Hỗn hợp, nhằm kiểm soát thí nghiệm. Cách này giúp đánh giá rõ chất lượng phân đoạn khi đã có định vị sơ bộ đúng, nhưng chưa thay thế được tình huống người dùng thật tự vẽ hộp, nên kết quả hiện tại chưa đủ để nói về sử dụng thực tế. Em xem đây là một giới hạn cần nói thẳng.

**13. Kịch bản Lệch tâm được mô phỏng thế nào? Mô hình có đang học đúng loại nhiễu mà nó đã thấy không?**

Khóa luận dùng quy tắc dịch ngẫu nhiên bằng 0,30 kích thước hộp, áp dụng thống nhất trong cả huấn luyện và đánh giá. Đúng như hội đồng nghi ngờ, kết quả về độ ổn định chủ yếu cho thấy mô hình thích nghi tốt với đúng dạng sai lệch đã được mô phỏng trong huấn luyện, chứ chưa phải mọi dạng sai lệch chưa từng thấy trong thực tế. Em không mở rộng kết luận thành "ổn định với mọi dạng câu nhắc sai".

---

## D. Kiến trúc: PSG, CAD, bản đồ nhiệt Gaussian

**14. PSG là gì, làm nhiệm vụ gì?**

PSG là Prompt Spatial Gate, đặt ở bộ mã hóa. Nó dùng bản đồ nhiệt câu nhắc để điều biến đặc trưng theo không gian, tức là làm mô hình chú ý sớm hơn vào vùng được khoanh. Nhưng PSG không cắt bỏ hoàn toàn đặc trưng gốc, vì vẫn có kết nối dư để giữ thông tin ảnh.

**15. CAD là gì, làm nhiệm vụ gì?**

CAD là Conditional Attention Decoder, đặt ở các kết nối tắt của nhánh giải mã. Nó mở rộng cổng chú ý của Attention U-Net bằng cách đưa thêm đặc trưng câu nhắc vào tín hiệu điều khiển. Nhờ vậy, lúc khôi phục mặt nạ, mô hình vẫn dùng thông tin người dùng đã cung cấp, chứ không chỉ dựa vào đặc trưng ảnh.

**16. Vì sao dùng bản đồ nhiệt Gaussian dạng cao nguyên thay vì hộp nhị phân đơn giản? Vì sao gọi là "dạng cao nguyên"?**

Nếu dùng mặt nạ nhị phân đơn giản thì biên hộp khá cứng. Dạng cao nguyên giữ giá trị tương đối cao và đều trong toàn vùng bên trong hộp, không chỉ nhấn mạnh ở tâm như Gaussian thuần, sau đó phần biên mới được làm mềm bằng bộ lọc Gaussian. Cách này vừa giữ thông tin trên toàn vùng câu nhắc, vừa tránh biên cứng, giúp mô hình bớt phụ thuộc vào ranh giới cứng của hộp. Kết quả ablation cho thấy lợi ích này rõ nhất ở kịch bản Lệch tâm, khi câu nhắc không còn lý tưởng.

**17. PSG khi dùng riêng cải thiện rất nhỏ, vậy có phải vai trò của nó bị phóng đại không?**

Đúng là nếu dùng riêng thì PSG cải thiện không lớn, nên em không nói quá về nó như một thành phần tự đứng là đủ. PSG không được đưa vào để tự nó nâng kết quả lên nhiều, mà để đưa thông tin câu nhắc vào bộ mã hóa từ sớm. Vai trò của nó rõ hơn khi kết hợp với CAD. Nói cách khác, em xem PSG là thành phần nền trong sự phối hợp, không phải thành phần "một mình cân" để tạo cải thiện lớn.

**18. CAD được cho là quan trọng nhất, nhưng ở kịch bản Bao trọn nó không phải lúc nào cũng tốt nhất. Vậy có mâu thuẫn không? Bằng chứng nào mạnh nhất cho CAD?**

Không mâu thuẫn, vì mục tiêu thiết kế của CAD không phải là tối ưu hóa trường hợp hộp giới hạn lý tưởng, mà là giữ hiệu năng khi câu nhắc bị sai lệch. Bằng chứng mạnh nhất nằm ở kịch bản Lệch tâm trên cả hai bộ dữ liệu: so với cấu hình dùng PSG và cổng chú ý nguyên bản, PGA-UNet dùng CAD tăng Dice khoảng 0,1065 trên BTXRD và 0,0924 trên FracAtlas, đều có p < 0,001. Vì vậy em không đánh giá CAD chỉ bằng một kịch bản lý tưởng duy nhất; có một đánh đổi nhỏ ở trường hợp lý tưởng để đổi lấy lợi thế rõ hơn khi câu nhắc bị lệch.

**19. Bằng chứng nào mạnh nhất cho vai trò của bản đồ nhiệt Gaussian?**

Cũng ở kịch bản Lệch tâm. So với PGA-UNet dùng câu nhắc nhị phân, phiên bản Gaussian tăng khoảng 0,0990 Dice trên BTXRD và 0,1005 trên FracAtlas, đều với p < 0,001. Điều này cho thấy Gaussian hữu ích nhất khi câu nhắc không còn lý tưởng.

**20. Mô hình của bạn có phải chỉ học cách bám theo hộp giới hạn không?**

Mô hình có sự phụ thuộc vào câu nhắc, và đó là chủ đích của bài toán. Tuy nhiên, mục tiêu không phải là bám cứng vào hộp, mà là sử dụng câu nhắc theo cách mềm hơn và ổn định hơn. Gaussian, PSG và CAD được đưa vào chính là để giảm phụ thuộc quá cứng vào ranh giới hộp.

---

## E. Thống kê và chỉ số đánh giá

**21. Kiểm định Wilcoxon có 36 phép so sánh mà chưa hiệu chỉnh multiple testing, vậy có đáng tin không?**

Em dùng Wilcoxon để bổ sung bằng chứng ở cấp độ ảnh, nhưng không diễn giải tất cả các giá trị p theo cùng mức độ. Report nói rõ bằng chứng mạnh hơn là các kết quả p < 0,001, còn các mức gần 0,05 chỉ được xem theo hướng thăm dò. Em không dùng bảng này để khẳng định quá mức, mà để hỗ trợ các xu hướng đã thấy rõ từ chênh lệch Dice trung bình.

**22. Vì sao không chỉ dùng Dice mà còn dùng cả IoU, Precision, Recall, HD95, CBL?**

Vì một chỉ số không phản ánh hết chất lượng phân đoạn. Dice và IoU đo chồng lấp. Precision và Recall cho biết xu hướng dự đoán rộng hay hẹp. HD95 phản ánh sai lệch đường biên. CBL là chỉ số bổ sung để xem độ lệch tâm giữa mặt nạ dự đoán và nhãn gốc, nhất là trong kịch bản câu nhắc bị lệch.

**23. CBL là gì và vì sao dùng nó?**

CBL là Center-Based Localization. Nó đo mức độ gần nhau giữa vị trí trung tâm của dự đoán và nhãn gốc. Vì khóa luận quan tâm đến độ ổn định dưới sai lệch câu nhắc, CBL giúp nhìn thêm về mặt định vị, không chỉ nhìn chồng lấp.

**24. HD95 được xử lý thế nào khi mặt nạ rỗng?**

Nếu cả dự đoán và nhãn đều rỗng thì HD95 được gán 0. Nếu chỉ một trong hai rỗng thì HD95 được gán giá trị phạt bằng kích thước cạnh ảnh, tức 256 hoặc 512 điểm ảnh. Cách này giúp không phải loại mẫu khỏi phép tính trung bình.

**25. Kết quả 4-fold cross-validation nói lên điều gì?**

Nó cho thấy kết quả của PGA-UNet không biến động quá nhiều khi thay đổi cách chia dữ liệu. Độ lệch chuẩn Dice trên BTXRD vào khoảng 0,0087 đến 0,0119, còn trên FracAtlas vào khoảng 0,0064 đến 0,0084. Điều này gợi ý mô hình khá ổn định, dù chưa thay thế được việc lặp lại với nhiều seed khởi tạo khác nhau.

---

## F. Kết quả chính

**26. Kết quả chính nổi bật nhất của bạn là gì?**

Trên BTXRD ở 512×512, PGA-UNet đạt Dice 0,8607, còn U-Net là 0,4740. Khi câu nhắc bị lệch tâm, PGA-UNet vẫn giữ Dice 0,8423. Ở phép so sánh cùng điều kiện với SAM-Med2D tại 256×256, PGA-UNet đạt Dice 0,8433 so với 0,7541 của SAM-Med2D trên BTXRD. Trên FracAtlas, mô hình giữ cùng xu hướng và đạt Dice 0,8169 ở kịch bản Bao trọn.

---

## G. Gatekeeper

**27. Gatekeeper có phải là đóng góp chính của khóa luận không?**

Không. Gatekeeper chỉ là thử nghiệm mở rộng để xem nếu đặt PGA-UNet trong một luồng xử lý có cả ảnh bình thường và bệnh lý thì điều gì xảy ra. Đóng góp kiến trúc chính vẫn là PGA-UNet.

**28. Kết quả Gatekeeper trên BTXRD và FracAtlas ra sao?**

Trên BTXRD, Gatekeeper đạt AUC-ROC 0,9421, Sensitivity 89,30%, Specificity 86,17%. Khi đưa vào luồng hai giai đoạn, Dice toàn luồng giảm từ 0,8626 trên ảnh được chuyển đúng xuống 0,6763 vì có lỗi định tuyến. Trên FracAtlas, AUC-ROC là 0,9132, Sensitivity chỉ còn 70,83%, Specificity 91,99%. Dice toàn luồng giảm còn 0,4230, chủ yếu do bỏ sót 21/72 ảnh bệnh lý.

**29. Gatekeeper làm giảm Dice toàn luồng khá mạnh, vậy giá trị thực tế của thử nghiệm này là gì? Vì sao Gatekeeper không nên tự động quyết định hoàn toàn?**

Giá trị của nó không nằm ở chỗ "hệ thống đã sẵn sàng dùng", mà ở chỗ nó làm rõ một điểm rất thực tế: nếu bước sàng lọc sai, đặc biệt là bỏ sót ảnh bệnh lý, thì mô-đun phân đoạn phía sau có tốt đến đâu cũng không cứu được toàn luồng. Kết quả trên cả BTXRD và FracAtlas đều cho thấy điều đó. Vì vậy Gatekeeper chỉ nên là công cụ hỗ trợ ưu tiên, không phải bộ lọc tự động để tự quyết định; quyết định chuyển bước vẫn cần người dùng chuyên môn xác nhận.

---

## H. Giới hạn và các câu hỏi xoáy khó

**30. Bạn có thể kết luận mô hình tổng quát hóa liên miền không?**

Không. Khóa luận chỉ cho thấy khi huấn luyện lại riêng trên FracAtlas thì xu hướng kết quả chính vẫn được giữ. Đó là bằng chứng về tính nhất quán của thiết kế trên hai miền dữ liệu, chứ chưa phải tổng quát hóa liên miền theo nghĩa huấn luyện trên một miền rồi suy luận trực tiếp trên miền chưa thấy.

**31. Kết quả của bạn có bị phụ thuộc vào câu nhắc quá nhiều không?**

Có phụ thuộc, và khóa luận không phủ nhận điều đó. Mô hình được thiết kế dùng cho bài toán đã có định vị sơ bộ. Điểm quan trọng hơn là thay vì chỉ bám cứng vào hộp, PGA-UNet cố gắng sử dụng câu nhắc theo cách mềm hơn và ổn định hơn dưới sai lệch, nhờ Gaussian, PSG và CAD.

**32. Vì sao không thử nghiệm với bác sĩ thật?**

Đó là hướng tiếp theo quan trọng nhất, nhưng nằm ngoài phạm vi và nguồn lực của khóa luận này. Để làm nghiêm túc thì cần có quy trình hợp tác với người có chuyên môn, dữ liệu phù hợp và tiêu chí đánh giá thao tác. Vì vậy em chọn cách mô phỏng có kiểm soát trước, rồi để đánh giá với người dùng thật làm bước tiếp theo.

**33. Kết quả nào bạn tự tin nhất? Điểm yếu nhất của khóa luận là gì?**

Phần em tự tin nhất là bằng chứng cho khả năng giữ hiệu năng khi câu nhắc bị sai lệch, đặc biệt ở kịch bản Lệch tâm; xu hướng này lặp lại trên cả BTXRD và FracAtlas, và có kiểm định Wilcoxon hỗ trợ cho CAD và Gaussian. Điểm yếu nhất là chưa có đánh giá với câu nhắc do người dùng thật cung cấp, chưa kiểm tra trên dữ liệu ngoài môi trường công khai, và chưa có bằng chứng cho tổng quát hóa liên miền theo nghĩa chặt. Ngoài ra một số cấu hình (SAM-Med2D tinh chỉnh, Gatekeeper) chỉ chạy một lần nên chưa có ước lượng phương sai qua nhiều lần khởi tạo.

**34. Nếu hội đồng hỏi một câu chốt để bảo vệ giá trị của khóa luận, bạn trả lời sao?**

Em sẽ trả lời là khóa luận không cố gắng chứng minh đã giải quyết xong bài toán phân đoạn X-quang xương trong thực tế. Giá trị chính của nó là đề xuất và kiểm tra một thiết kế CNN gọn nhẹ, có thể khai thác hộp giới hạn một cách ổn định hơn dưới sai lệch câu nhắc, và điều này đã được thể hiện khá rõ qua ablation và kết quả trên hai bộ dữ liệu.

---

## Chiến thuật khi trả lời

- Nếu bị hỏi xoáy về công bằng so sánh: nhắc lại "so sánh tổng thể" (lợi ích của có câu nhắc) và "ablation cùng điều kiện" (đóng góp kiến trúc thật).
- Nếu bị hỏi về leakage: thừa nhận đúng mức, không cố phủ nhận một giới hạn mình chưa kiểm chứng (cấp độ bệnh nhân).
- Nếu bị hỏi về thống kê: ưu tiên nói về xu hướng nhất quán + p < 0,001, tránh nói quá đà với các p gần 0,05.
- Nếu bị hỏi về tính mới: bám vào PSG + CAD + Gaussian và kịch bản Lệch tâm.
- Nếu bị hỏi về giá trị thực tế: nhấn mạnh "hướng hỗ trợ", không nhận đây là hệ thống lâm sàng hoàn chỉnh.
- Nếu bị hỏi xoáy thêm ngoài dự kiến: ưu tiên bám vào ba điểm neo: phạm vi bài toán, điều kiện so sánh, giới hạn đã nêu trong report.
- Nếu không chắc chắn, có thể trả lời theo mẫu: "Trong phạm vi khóa luận, em mới kết luận đến mức độ này; phần còn lại là hướng tiếp theo."

## Cách tập luyện

- Mỗi câu, đọc ý chính trước, không học thuộc từng chữ.
- Luyện nói thành tiếng, mỗi câu trả lời gói gọn trong khoảng 20-30 giây.
- Câu chốt ngắn khi bị vặn (dùng được bất cứ lúc nào cần):
  - "Khóa luận không khẳng định đây là hệ thống lâm sàng hoàn chỉnh; phạm vi là phân đoạn có hướng dẫn bằng hộp giới hạn."
  - "So sánh với U-Net và Attention U-Net là để cho thấy lợi ích của thiết lập có câu nhắc; còn đóng góp kiến trúc được kiểm tra công bằng hơn trong ablation."
  - "Bằng chứng mạnh nhất của thiết kế nằm ở kịch bản Lệch tâm, tức khả năng giữ hiệu năng khi câu nhắc không còn lý tưởng."
  - "Gatekeeper chỉ là mô-đun hỗ trợ; chính kết quả của khóa luận cũng cho thấy không nên để nó tự quyết hoàn toàn."
