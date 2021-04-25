from requests import get, post, delete

print(get('http://127.0.0.1:8080/api/films'))


"""запрос для получения фильмов"""
# корректный
print(get('http://127.0.0.1:8080/api/v2/films/1').json())
# не корректный
print(get('http://127.0.0.1:8080/api/v2/films').json())


"""добавление новой фильмов с помощью POST-запроса"""
# не корректно
print(post('http://127.0.0.1:8080/api/v2/films').json())
# не корректно
print(post('http://127.0.0.1:8080/api/v2/films',
           json={'title': 'Заголовок'}).json())
# корректно
print(post('http://127.0.0.1:8080/api/v2/films',
           json={'title': 'Заголовок',
                 'genres': 'Жанры',
                 'link_img': 'https://kinopoisk-ru.clstorage.net/1Q61eq136/69a6f60XrIfi/FQHxLRhppxAgJCFqbFV9x4jVN87DAmM18WubUJk4Cu_-OA5Ya_Et8AClhvuBalxoRIcam4h9_K6vN6w5xnhDx5ERpNmsrDLFwVAkD9lwPBZ9IObaB4dXdCBenrVrywhs3K8sO5lzLzYUkbIKVJ-J3EWSjyrtjHiaaBHNCbJPhPJH09BsvcjkIWY1IhgPZ-5SKvVHulBzM1Pi25kgikna_g7sPkjZAg32pSPzTZbPyV6W0j6prBope2sgqWsQXLZixqGyba_r58A25SHYT7eucgondypBUOIyAsqr0tsp623unsw6GaNs5Ldgcl-m_dkedKLcmP4aOsu4s0oqwG_m4FZSoW5cq-RzNCWAS90UbyHI5yXLkyIgAaPoayLrOmj_bY3sqJqj_rXEQ_Jux34p7oRgbui_yCmrGtIKW0LdB4OGYwE9fmh1wnQVM_vO9Z6gegQn-qOgQMNSmnjDKRhaH18sP-h7Il-3t4LR7lZ8WXz38o063cp76ZvxWCmhH9bhRDOArF-qFDHVxxO73icPwzsGV5ty0lBTsuk6MOj6Gv2_z45ZuTEe5sWw4P7ljjmPNQP9y5woyplIgatJ8-7WstZwcl1cKtZiFIURy6wGjQEJVHWrobLiMzDb2sA6uOluLm49ahty3wVlEPNM5g95fMazTvp-Wlt5SNMZKQNMREBG4UBO_NplYYS3YFifNk_DGQV06ONAkDAwymmCGqvK_h5-zhibUf1Ft6DRTqTPCm2UUw1Kr1uLO3nS2IkS3naTZSDSnqxrtQH2VSJZn3dc0SlmBpphENFBE1kbAOqYGq4sT03qGyAv9GeTkV5Wj0oNJMHeyp9b-qoLoNmbQA8GcvUDc20uGveTh9SiS843_DEKR1eKYuIRQlM7ajA66sl93A4uansh_TV3cmPvtK5JvpSz3vtvWZlpWpEqSPEf9tL1IYCMjLmkYEdFoEm8V59zyEREWNEAUWIy65rDyqm5PB5s7gmbwT2UJXKBTzZ_ml2X8O7rH2iquGiSu5txjaZxRcGTjj-ZN3PUBWFobmRfMlgV5bsjgSEjkaopY3momkwu3IxIi_E9xMUB8u31fgleNHCt6F-aGZnLoIuYot0HkkdzQ30fCeej1Ibw-sxHDuBbRDbosnCiY8N5ecBJmDgNbj6fa9lBvZRG0IPc9SxLLuSBTXsOKAkZyXALeTIt5LF3AMIujDhUw_Z2gcu8VH1gGPZkSUNREFCBSUkj-6loX6_dTbnJsX62BYDiXNbN6XxXog3JrYqI-rqyezkyL4YwZwEBPqxqZ6N2V0H6PmfPAFjnR6iToGKTEPv50uuoaM1ezc4JuKP_5uWhUTzlT9vcduMMu4_6itgpMzsZQi6lIIbTYx4c6jZTxFfxCCy1bxMKBleac1FgsLCrq6IIiYgcve9f2MpyLDak0nAPJRxKbzeijhivSIiZyuDKqqBtlAM0kPCenfgEQ2Qk8epMpQ9S6VcV-zEg4CJAekkRWWh6Pl8N76rr8d30JcDRDfat6c3XEUz7jyi66nmg6brxHGYBpINjHN0bhjOGF9AKDbZ-w0lF1ftjQ3AjwltY4Sgayf2OXjzbGNIOx1XwYm7U3Ugf1oNPi-1oSvlY4MmYc04mM6ZQgo9u-RbCJEazad2HvoDKFbRosVGSQGLoCCA4y-jt7M3u2ZjR7DR1QFGdp097DKYgnUqdSxvKKnB4GZPOBrFH49MPHNr0EUSVETgdtU7AOOZmCIOQUSHQ-WjDanvKLO2uj1s6o28GFuKznfTca12WY08Z7Ym7iXkgibhjjZQBlSBzfYy5BgEGRLIa_zfsExj2ReuTksIQozkZAQhISRysTr44mIBvVjVQoP6Gf1tcN4K_Ok9ZujuKQgvJ8k-UsYaxcix_2uZxRvWAaR5mrpJ5ZiSqQVBQMTMYOoNLO8oMfY6OKFtATwZEsrEv1zxZT8XirVleufraGqOr2LAtlBF2MVFen-lGQcVks8gtZ47COpWk2EDRsKNgyKiQGpvZ_A-MrUp5gT70J4Oj3uRtKg8U40yKX6iq-ilQGzswTjTgtXMBTE-4VRB1hQGr_nfdYzsltHrAUiMycOpI0UhbuR69_8z6a_GtBsXSA7wXDQt_tsFvSr2LuKu5UoloY20U8QZjkq1e6NUj9eUhaEx3zzEoRxfoQhMx0aL7iMFaWeifvKyciNjjjSe3EcJM5L87jMTh7YksOsmIafFbmXOvpqOXU_DMPetEwZfEM6huZ-5wGUX1iIJwADNCSjqyuliqnG2Pn0pr8D2WlSBDLRbeiL0kIyyrDKpZWHlCGikRnsYSF3DQjE6519K29UOLDTevMej2dCpBUHMDgzmKkAiZ2gz-7L6IqJBtNkUhkB-UrHuuF4Fsqu-Z-YsrEmh7YZwGs2XBUG0uCOYQNneiCLyl3UB4d7fKEjJCEaKL2wKLaugOng_tmDizjeaHYHIsBR47rOfy7Nlt2vqbuSGZmVGs9gA3QkCejfr2EHSk0OgNVn9RO5QV6NPgQiPiyelT6Vh4jb_P_2h5QS2GhwKTrScMO93l4p1Yf6qo6HthainALeXSRpBwf6z4JiOUpJOb3taOojjkV_qAYOExMSh5UgroaE-_DbxJyrH_9aSy0Q3EjeleVxE86W0J6RirMwgIs96GU3bQ4Y8OuScCdAQway7VzKMptuW5cBJTQeDL6IELSllf7iy9qOqBDoX3kuIttm36vabjL2lt67iouaLLewM_BBAmEbMvbAk0IfXW01mPRZ0xqwWHiRBgo-BjShqhORu7PN38n2nYwX8UZQIxHEccu250Eo6br_gJGamg-jkjrBezZrEQ3p2r9NI0lSAI3FfvITs1dmsB8AJBMvtK4Tl46X5ebp5o2dHP99TSgf6kHlv_96NuOp-oChvIkvuL0A02wmdywO5su4YiN7SQaJx2HWPahuf4oVDCo3OrmxFoymhsnk1eeltBTfTV0_FO9gwbDTWyLMt8qhkrw',
                 'age': 5}).json())


"""удаление фильмов"""
# не корректно
print(delete('http://127.0.0.1:8080/api/v2/films/999').json())
# корректно
# print(delete('http://127.0.0.1:8080/api/v2/films/9').json())
