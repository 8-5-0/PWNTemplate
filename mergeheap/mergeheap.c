__int64 (**init_proc())(void)
{
  __int64 (**result)(void); // rax

  result = &_gmon_start__;
  if ( &_gmon_start__ )
    result = _gmon_start__();
  return result;
}


__int64 (**init_proc())(void)
{
  __int64 (**result)(void); // rax

  result = &_gmon_start__;
  if ( &_gmon_start__ )
    result = _gmon_start__();
  return result;
}


void sub_850()
{
  JUMPOUT(&dword_0);
}


void sub_850()
{
  JUMPOUT(&dword_0);
}


void free(void *ptr)
{
  free(ptr);
}


char *strcpy(char *dest, const char *src)
{
  return strcpy(dest, src);
}


int puts(const char *s)
{
  return puts(s);
}


void __noreturn __stack_chk_fail()
{
  _stack_chk_fail();
}


void setbuf(FILE *stream, char *buf)
{
  setbuf(stream, buf);
}


int printf(const char *format, ...)
{
  return printf(format);
}


unsigned int alarm(unsigned int seconds)
{
  return alarm(seconds);
}


ssize_t read(int fd, void *buf, size_t nbytes)
{
  return read(fd, buf, nbytes);
}


void *malloc(size_t size)
{
  return malloc(size);
}


int atoi(const char *nptr)
{
  return atoi(nptr);
}


char *strcat(char *dest, const char *src)
{
  return strcat(dest, src);
}


void __noreturn exit(int status)
{
  exit(status);
}


__int64 _cxa_finalize()
{
  return __cxa_finalize();
}


__int64 _cxa_finalize()
{
  return __cxa_finalize();
}


__int64 (**sub_960())(void)
{
  __int64 (**result)(void); // rax

  result = &unk_202010;
  if ( &unk_202010 != &unk_202010 )
  {
    result = &ITM_deregisterTMCloneTable;
    if ( &ITM_deregisterTMCloneTable )
      result = ITM_deregisterTMCloneTable();
  }
  return result;
}


__int64 sub_9A0()
{
  return 0LL;
}


__int64 (**sub_9F0())(void)
{
  __int64 (**result)(void); // rax

  if ( !byte_202048 )
  {
    if ( &__cxa_finalize )
      _cxa_finalize();
    result = sub_960();
    byte_202048 = 1;
  }
  return result;
}


__int64 sub_A30()
{
  return sub_9A0();
}


__int64 menu()
{
  puts("1.add");
  puts("2.show");
  puts("3.dele");
  puts("4.merge");
  puts("5.exit");
  printf(">>");
  return get_num();
}


unsigned int sub_AA1()
{
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
  return alarm(0x3Cu);
}


__int64 __fastcall sub_AEE(__int64 a1, unsigned int a2)
{
  char buf; // [rsp+13h] [rbp-Dh]
  unsigned int i; // [rsp+14h] [rbp-Ch]
  unsigned __int64 v5; // [rsp+18h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  buf = 0;
  for ( i = 0; i < a2; ++i )
  {
    read(0, &buf, 1uLL);
    if ( buf == '\n' )
    {
      buf = 0;
      *(a1 + i) = 0;
      return i;
    }
    *(a1 + i) = buf;
  }
  return a2;
}


int sub_B8B()
{
  char nptr; // [rsp+0h] [rbp-20h]
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  read_safe(&nptr, 0xAu);
  return atoi(&nptr);
}


int add()
{
  signed int i; // [rsp+8h] [rbp-8h]
  int v2; // [rsp+Ch] [rbp-4h]

  for ( i = 0; i <= 14 && heaps[i]; ++i )
    ;
  if ( i > 14 )
    return puts("full");
  printf("len:");
  v2 = get_num();
  if ( v2 < 0 || v2 > 1024 )
    return puts("invalid");
  heaps[i] = malloc(v2);
  printf("content:");
  read_safe(heaps[i], v2);
  size[i] = v2;
  return puts("Done");
}


int show()
{
  int result; // eax
  int v1; // [rsp+Ch] [rbp-4h]

  printf("idx:");
  v1 = get_num();
  if ( v1 >= 0 && v1 <= 14 && heaps[v1] )
    result = puts(heaps[v1]);
  else
    result = puts("invalid");
  return result;
}


int dele()
{
  _DWORD *v0; // rax
  int v2; // [rsp+Ch] [rbp-4h]

  printf("idx:");
  v2 = get_num();
  if ( v2 >= 0 && v2 <= 14 && heaps[v2] )
  {
    free(heaps[v2]);
    heaps[v2] = 0LL;
    v0 = size;
    size[v2] = 0;
  }
  else
  {
    LODWORD(v0) = puts("invalid");
  }
  return v0;
}


int merge()
{
  int v1; // ST1C_4
  signed int i; // [rsp+8h] [rbp-18h]
  int v3; // [rsp+Ch] [rbp-14h]
  int v4; // [rsp+10h] [rbp-10h]

  for ( i = 0; i <= 14 && heaps[i]; ++i )
    ;
  if ( i > 14 )
    return puts("full");
  printf("idx1:");
  v3 = get_num();
  if ( v3 < 0 || v3 > 14 || !heaps[v3] )
    return puts("invalid");
  printf("idx2:");
  v4 = get_num();
  if ( v4 < 0 || v4 > 14 || !heaps[v4] )
    return puts("invalid");
  v1 = size[v3] + size[v4];
  heaps[i] = malloc(v1);
  strcpy(heaps[i], heaps[v3]);
  strcat(heaps[i], heaps[v4]);
  size[i] = v1;
  return puts("Done");
}


void __fastcall main(__int64 a1, char **a2, char **a3)
{
  __int64 savedregs; // [rsp+10h] [rbp+0h]

  init_0();
  while ( 1 )
  {
    menu();
    switch ( &savedregs )
    {
      case 1u:
        add();
        break;
      case 2u:
        show();
        break;
      case 3u:
        dele();
        break;
      case 4u:
        merge();
        break;
      case 5u:
        exit(0);
        return;
      default:
        continue;
    }
  }
}


void __fastcall init(unsigned int a1, __int64 a2, __int64 a3)
{
  __int64 v3; // r15
  signed __int64 v4; // rbp
  __int64 v5; // rbx

  v3 = a3;
  v4 = &off_201D68 - &off_201D60;
  init_proc();
  if ( v4 )
  {
    v5 = 0LL;
    do
      (*(&off_201D60 + v5++))(a1, a2, v3);
    while ( v4 != v5 );
  }
}


void fini(void)
{
  ;
}


void term_proc()
{
  ;
}


void term_proc()
{
  ;
}


